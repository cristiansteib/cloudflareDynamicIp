try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pathlib import Path
import logging
import sys
import os


class ConfigReader:
    def __init__(self, path, testing_mode=False):
        self.testing_mode = testing_mode
        self.data = self._get_data(path)

    def _assert_config_file_exists(self, file_path):
        if not os.path.isfile(file_path):
            if self.testing_mode:
                print("Missing config file: " + file_path)
            else:
                logging.critical("Missing config file: " + file_path)
            exit(127)

    def _get_data(self, path):
        path_tokens_conf = str(Path(path) / 'tokens.conf')
        path_hosts_conf = str(Path(path) / 'hosts.conf')
        self._assert_config_file_exists(path_tokens_conf)
        self._assert_config_file_exists(path_hosts_conf)

        setting_tokens = configparser.ConfigParser()
        setting_tokens.read(path_tokens_conf)

        setting_hosts = configparser.ConfigParser({'type': 'A'})
        setting_hosts.read(path_hosts_conf)

        data = dict()
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
                try:
                    token_name = setting_hosts.get(host_name, 'token-name')
                except:
                    print("File: " + path_hosts_conf)
                    print('You forgot the "token-name" in the section ' + host_name)
                    exit(2)

                try:
                    data[token_name]['dns']['hosts'].extend((setting_hosts.get(host_name, 'host').split(',')))
                except KeyError:
                    print("File: " + path_hosts_conf)
                    print('Token "{0}" in the section "{1}" does not exists'.format(token_name, host_name))
                    exit(2)
                except:
                    print("File: " + path_hosts_conf)
                    print(sys.exc_info()[1])
                    exit(2)
                data[token_name]['dns']['type'] = setting_hosts.get(host_name, 'type')
            except:
                print(sys.exc_info()[1])
                exit(2)
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
