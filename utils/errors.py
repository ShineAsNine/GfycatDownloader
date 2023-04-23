class InvalidOutputTemplate(Exception):
    def __init__(self):
        self.message = "Invalid output template, enter a valid output template or leave blank to use the default"


class InvalidProfile(Exception):
    def __init__(self):
        self.message = "Invalid profile, check that the url/username is correct"


class InvalidCollection(Exception):
    def __init__(self):
        self.message = "Invalid collection url"


class ExpiredOrInvalidAuthKey(Exception):
    def __init__(self):
        self.message = "Auth key is expired or invalid"


class InvalidSingleGfyUrl(Exception):
    def __init__(self, url):
        self.message = "Auth key is expired or invalid"
        self.url = url
