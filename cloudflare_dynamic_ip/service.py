from pathlib import Path
import logging
import time
import json
import os
from cloudflareapi import cloudflare
from cloudflare_dynamic_ip.config import ConfigReader
from cloudflare_dynamic_ip.filecache import FileCache
from cloudflare_dynamic_ip import args
import http.client

FILE_TO_STORAGE_IP = '/opt/cloudflare-dynamic-ip/storage/IP' #FIXME: el problema esta cuando se corre mientras se desarrolla
fileCache = FileCache()  # Cache the ip in the ram to avoid IO


def get_public_ip():
    try:
        conn = http.client.HTTPSConnection("www.jsonip.com")
        conn.request('GET', '/')
        response = conn.getresponse().read()
        return json.loads(response.decode())['ip']
    except OSError:
        logging.error("Error on gathering public ip ")
        exit(2)


def set_ip(ip, auth_key: str, auth_email: str, dns_type, urls: list):
    cloudflare_api = cloudflare.CloudFlareApi(auth_key, auth_email)
    easy = cloudflare.EasyUpdate(cloudflare_api)
    for url in urls:
        try:
            x = easy.update_dns_ip(dns_name=url, newIP=ip, dns_type=dns_type)
            state = 'Success' if x['value'].json()['result']['content'] == ip else 'FAILED'
            logging.info(state + ' change for record "{0}" on {1}'.format(dns_type, url))
        except:
            logging.error(
                'FAILED to change IP for record "{0}" on {1} using token {2}'.format(dns_type, url, auth_key))


def set_ip_dry_run(ip, auth_key: str, auth_email: str, dns_type, urls: list):
    for url in urls:
        print("Using email {0} to change record '{1}' to {2} for host {3}".format(auth_email, dns_type, ip, url))


def get_last_ip():
    return fileCache.get(FILE_TO_STORAGE_IP)


def save_new_ip(ip):
    fileCache.set(FILE_TO_STORAGE_IP, ip)


def run(config, dry_run=False):
    current_ip = get_public_ip()
    if current_ip != get_last_ip():
        logging.info("New ip " + current_ip)
        all_hosts_data = config.get_token_with_all_hosts()
        for auth_email, auth_key, dns_type, hosts in all_hosts_data:
            if not dry_run:
                set_ip(current_ip, auth_key, auth_email, dns_type, hosts)
            else:
                set_ip_dry_run(current_ip, auth_key, auth_email, dns_type, hosts)
        save_new_ip(current_ip)


def main():
    arguments = args.parse_args()

    config = ConfigReader(str(Path(arguments.config_directory)), arguments.test)

    if arguments.test:
        # only run for test the config
        print("Config is ok")
        exit(0)

    if arguments.dry_run is False:
        log_dir = str(Path(arguments.log_directory) / 'cloudflare_dynamic_ip.log')
        logging.basicConfig(
            filename=log_dir,
            format='[%(levelname)s] %(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%m-%y %H:%M:%S')

    while True:
        run(config, dry_run=arguments.dry_run)
        if not arguments.demonize:
            break
        time.sleep(10)


if __name__ == "__main__":
    main()
