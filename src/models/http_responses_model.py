import hashlib


class HttpResponsesModel:
    def __init__(self):
        self.id = None
        self.crawl_id = None
        self.visit_id = None
        self.url = None
        self.method = None
        self.referrer = None
        self.response_status = None
        self.response_status_text = None
        self.is_cached = None
        self.headers = None
        self.channel_id = None
        self.location = None
        self.time_stamp = None
        self.content_hash = None

    def __hash__(self):
        a = hashlib.md5(self.url.encode() + self.method.encode() + self.referrer.encode() + str(self.response_status).encode())
        b = a.hexdigest()
        as_int = int(b, 16)
        return as_int

    def __eq__(self, other):
        return self.url == other.url and \
            self.method == other.method and \
            self.referrer == other.referrer and \
            self.response_status == other.response_status

    def __str__(self):
        return self.url + ", " + self.method + ", " + self.referrer + ", " + str(self.response_status)