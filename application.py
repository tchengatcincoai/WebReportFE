import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, make_response
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from bson.json_util import dumps
from utils.web_util import json_response, normalize_domain
from utils.datetime_util import epoch_to_datetime
from utils.email_util import send_feedback_email, TO_LIST
from utils.ip_util import is_china_ip
from db_bootstrap import SAMPLE_DB_DATA
from constants import DATE_FORMAT_MONTH, DATE_FORMAT, TRANSLATION_MAP, COOKIE_CHINA_FLAG

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
log = logging.getLogger(__name__)


def connect():
    client = MongoClient('localhost', 27017)
    db = client['WebReportDB']
    connection = db['WebReportCollection']
    return connection


application = Flask(__name__)
application.config['ELASTICSEARCH_URL'] = 'http://localhost:9200/'
es = Elasticsearch([application.config['ELASTICSEARCH_URL']])
mongodb_connection = connect()


def set_china_cookie(url):
    china_flag = is_china_ip(request.remote_addr)
    response = make_response(redirect(url))
    response.set_cookie(COOKIE_CHINA_FLAG, str(china_flag).lower())
    return response


@application.route('/')
def default_page():
    return redirect(url_for('index'))


@application.route('/index', endpoint='index')
def index_page():
    if COOKIE_CHINA_FLAG not in request.cookies:
        return set_china_cookie(request.url)
    else:
        china_flag = request.cookies[COOKIE_CHINA_FLAG]
        china_flag = china_flag == 'true'
        return render_template("index.html", china_flag=china_flag)


@application.route('/contact', endpoint='contact')
def contact_page():
    if COOKIE_CHINA_FLAG not in request.cookies:
        return set_china_cookie(request.url)
    else:
        china_flag = request.cookies[COOKIE_CHINA_FLAG]
        china_flag = china_flag == 'true'
        return render_template("contact.html", china_flag=china_flag)


@application.route('/feedback', endpoint='feedback', methods=['POST'])
def feedback():
    # TODO: send email does not work, may be the smtp issue???
    form = request.form
    username = form['name']
    sender = form['email']
    phone = form['phone']
    message = form['message']
    message += '\nPhone number: {phone}'.format(phone=phone)
    today = datetime.datetime.today().strftime(DATE_FORMAT)
    send_feedback_email(TO_LIST, sender,
                        'feedback from {user} on {curr_date}'.format(user=username, curr_date=today),
                        content=message)
    return redirect(url_for('index'))


@application.route('/bootstrap', endpoint='bootstrap')
def bootstrap():
    '''
    if collection is empty, insert some sample data for debug and test
    :return:
    '''
    one_record = mongodb_connection.find_one()
    if not one_record:
        mongodb_connection.insert(SAMPLE_DB_DATA)
        one_record = mongodb_connection.find_one()
    return json_response(dumps(one_record), 200)


@application.route('/cleanall', endpoint='cleanall')
def cleanall():
    '''
    delete all records in the collection
    :return:
    '''
    mongodb_connection.delete_many({})
    return json_response({'result': 'succeed'}, 200)


def web_data_initilize(keys):
    web_data = {}
    for key in keys:
        web_data[key] = {'data': [], 'last_change': None, 'color': 'green', 'direction': 'fa-sort-asc',
                         'y_low': None, 'y_high': None}
    return web_data


@application.route('/report', endpoint='report')
def report_page():
    if COOKIE_CHINA_FLAG not in request.cookies:
        return set_china_cookie(request.url)
    else:
        china_flag = request.cookies[COOKIE_CHINA_FLAG]
        china_flag = china_flag == 'true'
        web_address = request.args.get('website_address')
        if not web_address:
            return render_template("page_404.html", requested_url=" ")
        # normalize the url
        web_address = normalize_domain(web_address)
        one_record = mongodb_connection.find_one({"web_address": web_address})

        if not one_record:
            return render_template("page_404.html", requested_url=web_address)
        web_address = one_record['web_address']
        timestamps = []
        web_data = web_data_initilize(
            ['global_rank', 'load_time', 'page_views_per_visitor', 'daily_user'])
        for item in one_record['web_data']:
            timestamps.append(epoch_to_datetime(item['timestamp'], DATE_FORMAT_MONTH))
            web_data['global_rank']['data'].append(item['global_rank'])
            web_data['load_time']['data'].append(item['load_time'])
            web_data['page_views_per_visitor']['data'].append(item['page_views_per_visitor'])
            web_data['daily_user']['data'].append(item['daily_user'])
        # make y axises to be good for all metrics by setting y max and y min for each metric
        tmp_index = 0
        for item in web_data:
            min_value = min(web_data[item]['data'])
            max_value = max(web_data[item]['data'])
            diff_value = max_value - min_value
            web_data[item]['y_low'] = min_value - (0.1 + tmp_index) * diff_value
            web_data[item]['y_high'] = max_value + (0.1 + tmp_index) * diff_value
            # make y axises to be off by a little bit
            tmp_index += 0.01
        geo_contribution = one_record['web_data'][-1]['geo_contribution']
        top_key_words = one_record['web_data'][-1]['top_key_words']
        related_sites = one_record['web_data'][-1]['related_sites']
        upstream_sites = one_record['web_data'][-1]['upstream_sites']
        top_sites_linking_in = one_record['web_data'][-1]['top_sites_linking_in']
        where_do_visitors_go_on = one_record['web_data'][-1]['where_do_visitors_go_on']
        samples_count = len(one_record['web_data'])
        if samples_count > 1:
            for metric in web_data:
                diff = web_data[metric]['data'][samples_count - 1] - web_data[metric]['data'][samples_count - 2]
                if web_data[metric]['data'][samples_count - 2] == 0:
                    change = None
                else:
                    change = diff * 100.0 / web_data[metric]['data'][samples_count - 2]
                    if change < 0:
                        web_data[metric]['color'] = 'red'
                        web_data[metric]['direction'] = 'fa-sort-desc'
                if change is None:
                    change = 'N/A'
                else:
                    change = "{number}%".format(number=("%.2f" % change))
                web_data[metric]['last_change'] = change
        return render_template("report.html", web_address=web_address, web_data=web_data, timestamps=timestamps,
                               geo_contribution=geo_contribution, samples_count=samples_count,
                               top_key_words=top_key_words, related_sites=related_sites,
                               upstream_sites=upstream_sites, top_sites_linking_in=top_sites_linking_in,
                               where_do_visitors_go_on=where_do_visitors_go_on, china_flag=china_flag)


@application.template_filter('translation')
def _jinja2_filter_translation(in_string, china_flag):
    '''
    return translations, only english or chinese
    :param in_string: input string
    :param china_flag: true means to chinese, otherwise, to english
    :return: translated string
    '''
    if in_string in TRANSLATION_MAP:
        if china_flag:
            return TRANSLATION_MAP[in_string]['chinese']
        else:
            return TRANSLATION_MAP[in_string]['english']
    else:
        return in_string


if __name__ == '__main__':
    application.run(host='0.0.0.0')
