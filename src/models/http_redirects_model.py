import hashlib


class HttpRedirectsModel:
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

    def __eq__(self, other):
        return self.old_channel_id == other.old_channel_id
