class ConfigReader():

    def get_hosts(self, api_key_name):
        # search all the hosts for that api name
        pass

    def get_all_names(self):
        return []

    def get_key(self, api_key_name):
        return ""

    def get_email(self, api_key_name):
        return ""

    def get_key_with_all_hosts(self):
        all_data = []
        for api_name in self.get_all_names():
            all_data.append((self.get_email(api_name), self.get_key(api_name), self.get_hosts()))
        return all_data
