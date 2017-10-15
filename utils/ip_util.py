import logging
from utils.web_util import fetch_json_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
log = logging.getLogger(__name__)

TAOBAO_IP_SERVICE_URL = "http://ip.taobao.com/service/getIpInfo.php?ip="


def is_china_ip(ip):
    '''
    return is china ip or not
    :param ip: string, xxx.xxx.xxx.xxx
    :return: True or False
    '''
    cmd_url = '{service_url}{ip}'.format(service_url=TAOBAO_IP_SERVICE_URL, ip=ip)
    try:
        data = fetch_json_data(cmd_url)
        if not data or 'code' not in data or data['code'] == 1 or 'data' not in data:
            return False
        country_id = data['data']['country_id']
        return country_id == 'CN' or country_id == '86'
    except Exception as ex:
        log.exception(ex)
        return False