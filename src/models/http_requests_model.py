import hashlib
import re


class HttpRequestsModel:
    regex = re.compile('.*(\.net|\.com|\.org|\.ca|\.eu|\.edu|\.io|\.fi|\.fr|\.tv|\.ru|\.co)')

    def __init__(self):
        self.id = None
        self.crawl_id = None
        self.visit_id = None
        self.url = None
        self.top_level_url = None
        self.method = None
        self.referrer = None
        self.headers = None
        self.channel_id = None
        self.is_XHR = None
        self.is_frame_load = None
        self.is_full_page = None
        self.is_third_party_channel = None
        self.is_third_party_window = None
        self.triggering_origin = None
        self.loading_origin = None
        self.loading_href = None
        self.req_call_stack = None
        self.content_policy_type = None
        self.post_body = None
        self.time_stamp = None

    def __hash__(self):
        url = self.url.split('//')[1]
        url = url.split('/')[0]
        a = hashlib.md5(url.encode() + self.referrer.encode())
        b = a.hexdigest()
        as_int = int(b, 16)
        return as_int

    def __eq__(self, other):
        url1 = self.url.split('//')[1]
        url1 = url1.split('/')[0]

        url2 = other.url.split('//')[1]
        url2 = url2.split('/')[0]

        return url1 == url2 and self.referrer == other.referrer

    def __str__(self):
        url1 = self.url.split('//')[1]
        url1 = url1.split('/')[0]
        url1 = re.search(self.regex, url1).group(0)
        return str(url1) + ": " + str(self.top_level_url)