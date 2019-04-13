from cloudflareapi import cloudflare
import requests
from config import ConfigReader
import logging

LOG_FILE = '/var/log/cloudflare_dynamic_ip.log'

def get_public_ip():
    url = "http://jsonip.com"
    response = requests.request(method='GET', url=url)
    return response.json()['ip']


def set_ip(ip, auth_key: str, auth_email: str, urls: list):
    cloudflare_api = cloudflare.CloudFlareApi(auth_key, auth_email)
    easy = cloudflare.EasyUpdate(cloudflare_api)
    for url in urls:
        x = easy.update_dns_ip(dns_name=url, newIP=ip)
        print(url, ' ', x['value'].text)


def get_last_ip():
    pass


def run():
    current_ip = get_public_ip()
    if current_ip is not get_last_ip():
        all_hosts_data = ConfigReader().get_key_with_all_hosts()
        for auth_key, auth_email, urls in all_hosts_data:
            set_ip(current_ip, auth_key, auth_email, urls)


if __name__ == "__main__":
    logging.basicConfig(
        filename=LOG_FILE, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    run()
