class HttpRequestsModel:
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
