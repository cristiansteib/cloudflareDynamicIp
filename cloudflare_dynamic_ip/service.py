import requests
from pathlib import Path
import logging

from cloudflareapi import cloudflare
from config import ConfigReader
import args


def get_public_ip():
    url = "http://jsonip.com"
    response = requests.request(method='GET', url=url)
    return response.json()['ip']


def set_ip(ip, auth_key: str, auth_email: str, urls: list):
    cloudflare_api = cloudflare.CloudFlareApi(auth_key, auth_email)
    easy = cloudflare.EasyUpdate(cloudflare_api)
    for url in urls:
        x = easy.update_dns_ip(dns_name=url, newIP=ip)
        logging.info(url + ' ' + x['value'].text)


def set_ip_dry_run(ip, auth_key: str, auth_email: str, urls: list):
    for url in urls:
        print("Using email {0}, set ip {1} for host {2}".format(auth_email, ip, url))


def get_last_ip():
    pass


def run(config, dry_run=False):
    current_ip = get_public_ip()
    if current_ip is not get_last_ip():
        logging.info("Ip change " + current_ip)
        all_hosts_data = config.get_key_with_all_hosts()
        for auth_key, auth_email, urls in all_hosts_data:
            if not dry_run:
                set_ip(current_ip, auth_key, auth_email, urls)
            else:
                set_ip_dry_run(current_ip, auth_key, auth_email, urls)


if __name__ == "__main__":
    args = args.parse_args()
    config = ConfigReader(str(Path(args.config_directory)))

    if args.dry_run is False:
        log_dir = str(Path(args.log_directory) / 'cloudflare_dynamic_ip.log')
        logging.basicConfig(
            filename=log_dir,
            filemode='w',
            format='%(asctime)s - %(message)s', level=logging.INFO)
    run(config, dry_run=args.dry_run)

