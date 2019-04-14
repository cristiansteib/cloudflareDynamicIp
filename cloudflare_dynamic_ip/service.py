from pathlib import Path
import logging
import time
import json
import os
from cloudflareapi import cloudflare
from config import ConfigReader
from filecache import FileCache
import args
import http.client

FILE_TO_STORAGE_IP = 'IP'
fileCache = FileCache()  # Cache the ip in the ram to avoid IO


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
            state = 'Success' if x['value'].json()['result']['content'] == ip else 'FAILED'
            logging.info(state + ' change for record "{0}" on {1}'.format(dns_type, url))
        except:
            logging.critical(
                'FAILED to change IP for record "{0}" on {1} using token {2}'.format(dns_type, url, auth_key))


def set_ip_dry_run(ip, auth_key: str, auth_email: str, dns_type, urls: list):
    for url in urls:
        print("Using email {0} to change record '{1}' to {2} for host {3}".format(auth_email, dns_type, ip, url))


def get_last_ip():
    return fileCache.get('IP')


def save_new_ip(ip):
    fileCache.set('IP', ip)


def run(config, dry_run=False):
    current_ip = get_public_ip()
    if current_ip != get_last_ip():
        logging.info("Ip change to " + current_ip)
        all_hosts_data = config.get_token_with_all_hosts()
        for auth_email, auth_key, dns_type, hosts in all_hosts_data:
            if not dry_run:
                set_ip(current_ip, auth_key, auth_email, dns_type, hosts)
            else:
                set_ip_dry_run(current_ip, auth_key, auth_email, dns_type, hosts)
        save_new_ip(current_ip)


if __name__ == "__main__":
    args = args.parse_args()
    config = ConfigReader(str(Path(args.config_directory)))

    if args.dry_run is False:
        log_dir = str(Path(args.log_directory) / 'cloudflare_dynamic_ip.log')
        logging.basicConfig(
            filename=log_dir,
            format='[%(levelname)s] %(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%m-%y %H:%M:%S')

    while True:
        run(config, dry_run=args.dry_run)
        if not args.demonize:
            break
        time.sleep(10)
