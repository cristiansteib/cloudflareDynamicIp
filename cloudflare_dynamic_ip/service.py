from pathlib import Path
import logging
import time
import json

from cloudflareapi import cloudflare
from config import ConfigReader
import args
import http.client


def get_public_ip():
    conn = http.client.HTTPSConnection("www.jsonip.com")
    conn.request('GET', '/')
    response = conn.getresponse().read()
    return json.loads(response)['ip']


def set_ip(ip, auth_key: str, auth_email: str, dns_type, urls: list):
    cloudflare_api = cloudflare.CloudFlareApi(auth_key, auth_email)
    easy = cloudflare.EasyUpdate(cloudflare_api)
    for url in urls:
        x = easy.update_dns_ip(dns_name=url, newIP=ip, dns_type=dns_type)
        try:
            state = 'success' if x['value'].json()['result']['content'] == ip else 'FAILED'
            logging.info(state + ' change for ' + url)
        except:
            logging.critical('FAIL change for ' + url + ' using token ' + auth_key)


def set_ip_dry_run(ip, auth_key: str, auth_email: str, dns_type, urls: list):
    for url in urls:
        print("Using email {0} to change record '{1}' to {2} for host {3}".format(auth_email, dns_type, ip, url))


def get_last_ip():
    pass


def _save_new_ip(ip):
    pass


def run(config, dry_run=False):
    current_ip = get_public_ip()
    if current_ip is not get_last_ip():
        logging.info("Ip change " + current_ip)
        all_hosts_data = config.get_token_with_all_hosts()
        for auth_email, auth_key, dns_type, hosts in all_hosts_data:
            if not dry_run:
                set_ip(current_ip, auth_key, auth_email, dns_type, hosts)
            else:
                set_ip_dry_run(current_ip, auth_key, auth_email, dns_type, hosts)
        _save_new_ip(current_ip)


if __name__ == "__main__":
    args = args.parse_args()
    config = ConfigReader(str(Path(args.config_directory)))

    if args.dry_run is False:
        log_dir = str(Path(args.log_directory) / 'cloudflare_dynamic_ip.log')
        logging.basicConfig(
            filename=log_dir,
            format='%(asctime)s - %(message)s', level=logging.INFO)

    while True:
        run(config, dry_run=args.dry_run)
        if not args.demonize:
            break
        time.sleep(10)

