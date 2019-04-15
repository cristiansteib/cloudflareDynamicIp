try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pathlib import Path
import logging


class ConfigReader:
    def __init__(self, path):
        self.data = self._get_data(path)

    @staticmethod
    def _get_data(path):
        data = dict()

        setting_tokens = configparser.ConfigParser()
        setting_tokens.read(Path(path) / 'tokens.conf')
        setting_hosts = configparser.ConfigParser({'type': 'A'})
        setting_hosts.read(Path(path) / 'hosts.conf')

        for token_name in setting_tokens.sections():
            token = setting_tokens.get(token_name, 'token')
            email = setting_tokens.get(token_name, 'email')
            data.setdefault(token_name,
                            {
                                'token': token,
                                'email': email,
                                'dns': {
                                    'type': '',
                                    'hosts': []
                                }
                            })

        for host_name in setting_hosts.sections():
            try:
                token_name = setting_hosts.get(host_name, 'token-name')
                data[token_name]['dns']['hosts'].extend((setting_hosts.get(host_name, 'host').split(',')))
                data[token_name]['dns']['type'] = setting_hosts.get(host_name, 'type')
            except KeyError:
                logging.ERROR("Bad config, missing some key? ", exc_info=True)
            except:
                logging.CRITICAL("Error parsing config", exc_info=True)
        return data


    def get_hosts(self, token_name):
        return self.data[token_name]['dns']['hosts']

    def get_dns_type(self, token_name):
        return self.data[token_name]['dns']['type']

    def get_all_token_names(self):
        return self.data.keys()

    def get_token(self, token_name):
        return self.data[token_name]['token']

    def get_email(self, token_name):
        return self.data[token_name]['email']

    def get_token_with_all_hosts(self):
        all_data = []
        for api_name in self.get_all_token_names():
            all_data.append((self.get_email(api_name),
                             self.get_token(api_name),
                             self.get_dns_type(api_name),
                             self.get_hosts(api_name))
                            )
        return all_data
