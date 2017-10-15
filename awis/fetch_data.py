import linecache   # usesd for read particular line of top-1m.csv
import pycurl
import re
import time
from StringIO import StringIO

import lxml
import pymongo
import xmltodict as xd

import awis

from WebReportFE.utils.web_util import normalize_domain

LOCAL_MONGO_CLUSTER='mongodb://warren:warren@cluster0-shard-00-00-kvqib.mongodb.net:27017,cluster0-shard-00-01-kvqib.mongodb.net:27017,cluster0-shard-00-02-kvqib.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
#LOCAL_MONGO_CLUSTER='mongodb://localhost:27017/'
READ_THIS_MANY = 500   # everytime we read this many entries in top-1m.csv
URL_FILE = 'top-1m.csv'

def get_mongo_client(cluster):
    client = pymongo.MongoClient(cluster)
    return client

def connect(client):
    db = client['WebReportDev']
    connection = db['WebReportCollectionDev']
    return connection

def get_db(client, db_name):
    return client[db_name]


def fetch_data(secret_file, domains=['dealsea.com']):
    """
    :param domain: list of domains we want to check on alexa
    :return: JSON object of alexa query
    """

    with open(secret_file, 'r') as f:
        content = f.readlines()

    AWSAccessKeyId = content[0].strip()
    AWSSecretKey = content[1].strip()

    api = awis.AwisApi(AWSAccessKeyId, AWSSecretKey)
    sample_db_data = []

    domains = []

    # First we look into magic_number.txt to find out up to which row in top-1m.csv we have queried
    with open('magic_number.txt') as f:
        upto = int(f.read())

    we_should_end = upto + READ_THIS_MANY
    for i in xrange(upto, we_should_end):
        data = linecache.getline(URL_FILE, i)
        data = data.strip()
        domains.append(data.split(',')[1])

    # Update magic_number.txt
    f = open('magic_number.txt', 'w')
    f.write(str(we_should_end))
    f.close()


    client = get_mongo_client(LOCAL_MONGO_CLUSTER)
    connection = connect(client)

    for domain in domains:
        try:
            print 'working on %s' % domain
            # First clean up the domain name, we only accept like google.com, so we should normalize our input
            domain = normalize_domain(domain)

            one_record = connection.find_one({'web_address' : domain})

            if not one_record:
                db_data = {}
                db_data['web_address'] = domain
                db_data['web_data'] = []
                connection.insert(db_data)


            db_data_web_data = {}
            db_data_web_data['timestamp'] = time.time()

            # Call url_info
            result = api.url_info(domain,
                                  'RelatedLinks',
                                  'Categories',
                                  'Rank',
                                  'RankByCountry',
                                  'UsageStats',
                                  'AdultContent',
                                  'Speed',
                                  'Language',
                                  'OwnedDomains',
                                  'LinksInCount',
                                  'SiteData')
            string_xml = lxml.etree.tostring(result.getroot())
            result_dict = xd.parse(string_xml)

            if result_dict['aws:UrlInfoResponse']['aws:Response']['aws:ResponseStatus']['aws:StatusCode'] != 'Success':
                print 'Not a successful info retrieval from Alexa for domain: ' % domain

            meat = result_dict['aws:UrlInfoResponse']['aws:Response']['aws:UrlInfoResult']['aws:Alexa']

            content_data = meat['aws:ContentData']
            db_data_web_data['load_time'] = float(content_data['aws:Speed']['aws:MedianLoadTime'])

            traffic_data = meat['aws:TrafficData']

            db_data_web_data['global_rank'] = int(traffic_data['aws:Rank'])
            db_data_web_data['geo_contribution'] = []
            for country in traffic_data['aws:RankByCountry']['aws:Country']:
                item = {}
                item['country'] = country['@Code']
                item['rank'] = country['aws:Rank']
                item['pageviews'] = float(country['aws:Contribution']['aws:PageViews'].replace('%', ''))
                item['users'] = float(country['aws:Contribution']['aws:Users'].replace('%', ''))
                db_data_web_data['geo_contribution'].append(item)

            # Up to here, db_data_web_data['geo_contribution'] should have all the data, we will sort them
            # in reverse order of pageviews, i.e., largest pageviews on top
            l = db_data_web_data['geo_contribution']
            db_data_web_data['geo_contribution'] = sorted(l, key=lambda k: k['pageviews'], reverse=True)

            # -1 is because the last item in this list is 1 Day UsageStatistics
            db_data_web_data['page_views_per_visitor'] = float(traffic_data['aws:UsageStatistics']['aws:UsageStatistic'][-1]['aws:PageViews']['aws:PerUser']['aws:Value'])

            # Deduce daily user from Reach. Reach uses number of users per million. We assume in the world, there are
            # 3.2 billion internet users. So total daily user = reach * 3200
            db_data_web_data['daily_user'] = int(traffic_data['aws:UsageStatistics']['aws:UsageStatistic'][-1]['aws:Reach']['aws:PerMillion']['aws:Value'].replace(',', '')) * 3200

            result = api.sites_linking_in(domain, 5)
            string_xml = lxml.etree.tostring(result.getroot())
            result_dict = xd.parse(string_xml)

            if result_dict['aws:SitesLinkingInResponse']['aws:Response']['aws:ResponseStatus']['aws:StatusCode'] != 'Success':
                print 'Failed to get SitesLinkingIn for domain: ' % domain
                continue
            db_data_web_data['top_sites_linking_in'] = []
            for item in result_dict['aws:SitesLinkingInResponse']['aws:Response']['aws:SitesLinkingInResult']['aws:Alexa']['aws:SitesLinkingIn']['aws:Site']:
                temp = {}
                temp['site'] = item['aws:Title']
                temp['page'] = item['aws:Url']
                db_data_web_data['top_sites_linking_in'].append(temp)

            consume_alexa_website(domain, db_data_web_data)

            connection.update({'web_address': domain}, {'$push': {'web_data': db_data_web_data}})
        except:
            print '%s cannot get data' % domain

def consume_alexa_website(url, db_data_web_data):
    target = 'https://www.alexa.com/siteinfo/%s' % url
    buf = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, target)
    c.setopt(c.WRITEDATA, buf)
    c.perform()
    c.close()

    body = buf.getvalue()

    # This is a hack to get top keyword percent of search traffic. It's not scalable, we need
    # to replace it to a better solution in the future.\
    # TODO: yezhang
    percent_search_traffic_str = r'(.*)Percent of Search(.*?)(<tbody>.*?<span class=\'table-data-order-number\'.*?' \
                                 r')\</tbody>.*'
    m = re.search(percent_search_traffic_str, body, re.M | re.I | re.S)
    percent_search_traffic_result = m.group(3)
    b = r'<td.*?><span.*?>.*?<\/span>.*?<span>(.*?)<\/span><\/td>.*?<td.*?><span.*?>(.*?)<\/span><\/td>'
    m = re.search(r'%s.*?%s.*?%s.*?%s.*?%s.*' % (b, b, b, b, b), percent_search_traffic_result, re.M|re.I|re.S)
    db_data_web_data['top_key_words'] = []
    # The m.group(1) ... mgroup(10) are the top 5 key words and their percent of search traffic
    # Notice that the value in dict is type of Float indicating percentage
    for i in xrange(1, 11, 2):
        db_data_web_data['top_key_words'].append({'keyword': m.group(i).replace('.', '^'), 'percent_of_search_traffic': float(m.group(i + 1).replace('%', ''))})

    similar_sites_str = r'(.*)Similar Websites by Audience Overlap(.*?)(<tbody>.*?<span class=\'table-data-order-number\'.*?)\</tbody>.*'
    m = re.search(similar_sites_str, body, re.M | re.I | re.S)
    similar_sites_result = m.group(3)
    b = r'<td.*?><span.*?>.*?<\/span>.*?<a href=.*?>(.*?)<\/a><\/td>'
    m = re.search(r'%s.*?%s.*?%s.*?%s.*?%s.*' % (b, b, b, b, b), similar_sites_result, re.M | re.I | re.S)
    db_data_web_data['related_sites'] = []
    for i in xrange(1, 6):
        db_data_web_data['related_sites'].append(m.group(i).replace('.', '^'))

    # Get upstream information
    db_data_web_data['upstream_sites'] = []
    upstream_sites_str = r'(.*)<span><strong>Upstream Sites<\/strong><\/span>(.*?)(<tbody>.*?<span class=\'table-data-order-number\'.*?)\<\/tbody>.*'
    m = re.search(upstream_sites_str, body, re.M | re.I | re.S)
    upstream_sites_result = m.group(3)
    b = r'<td.*?><span.*?>.*?<\/span>.*?<a href=.*?>(.*?)<\/a><\/td>.*?<td.*?><span.*?>(.*?)<\/span><\/td>'
    m = re.search(r'%s.*?%s.*?%s.*?%s.*?%s.*' % (b, b, b, b, b), upstream_sites_result, re.M | re.I | re.S)
    for i in xrange(1, 10, 2):
        db_data_web_data['upstream_sites'].append({'site': m.group(i).replace('.', '^'), 'percent_of_unique_visits': float(m.group(i + 1).replace('%', ''))})

    # Get 'Where do visitors go on xxx.com?' information
    db_data_web_data['where_do_visitors_go_on'] = []
    where_visitor_go_str = r'(.*)Where do visitors go on %s(.*?)(<tbody>.*?<span class=\'word-wrap\'.*?)\<\/tbody>.*' % (url.replace('.', '\.'))
    m = re.search(where_visitor_go_str, body, re.M | re.I | re.S)
    where_visitor_go_result = m.group(3)
    b = r'<td.*?><span.*?>(.*?)<\/span><\/td>.*?<td.*?><span.*?>(.*?)<\/span><\/td>'
    m = re.search(r'%s.*?%s.*?%s.*?%s.*?%s.*' % (b, b, b, b, b), where_visitor_go_result, re.M | re.I | re.S)
    for i in xrange(1, 10, 2):
        db_data_web_data['where_do_visitors_go_on'].append({'subdomain': m.group(i).replace('.', '^'), 'percent_of_visitors': float(m.group(i + 1).replace('%', ''))})


if __name__ == '__main__':
    # Change parameter of fetch_data() to '/Users/kieky/Documents/GitHub/freewebsitereport/WebReportFE/static/secret'
    # if run as tcheng@
    db_data = fetch_data('/Users/GelinZHU/aws_secret/secret.txt')
    client = get_mongo_client(LOCAL_MONGO_CLUSTER)
    db = client.test
