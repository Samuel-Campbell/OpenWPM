import hashlib
import re


class HttpRedirectsModel:
    regex = re.compile('.*(\.net|\.com|\.org|\.ca|\.eu|\.edu|\.io|\.fi|\.fr|\.tv|\.ru|\.co)')

    def __init__(self):
        self.id = None
        self.crawl_id = None
        self.visit_id = None
        self.old_channel_id = None
        self.new_channel_id = None
        self.is_temporary = None
        self.is_permanent = None
        self.is_internal = None
        self.is_sts_upgrade = None
        self.time_stamp = None

    def __hash__(self):
        if self.old_channel_id is None:
            return 0
        a = hashlib.md5(self.old_channel_id.encode())
        b = a.hexdigest()
        as_int = int(b, 16)
        return as_int

    def __str__(self):
        url1 = self.old_channel_id.url.split('//')[1]
        url1 = url1.split('/')[0]
        url1 = re.search(self.regex, url1).group(0)

        url2 = self.new_channel_id.url.split('//')[1]
        url2 = url2.split('/')[0]
        url2 = re.search(self.regex, url2).group(0)

        return url1 + ': ' + url2

    def __eq__(self, other):
        return self.old_channel_id == other.old_channel_id
