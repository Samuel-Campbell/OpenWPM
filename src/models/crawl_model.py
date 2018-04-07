import json


class CrawlModel:
    def __init__(self):
        self.crawl_id = None
        self.task_id = None
        self.browser_params = None
        self.screen_res = None
        self.ua_string = None
        self.finished = None
        self.start_time = None

    def __eq__(self, dictionary):
        d = json.loads(self.browser_params)
        if d == dictionary:
            return True
        return False