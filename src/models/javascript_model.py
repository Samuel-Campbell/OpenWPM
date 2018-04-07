import hashlib


class JavascriptModel:
    def __init__(self):
        self.id = None
        self.crawl_id = None
        self.visit_id = None
        self.script_url = None
        self.script_line = None
        self.script_col = None
        self.func_name = None
        self.script_loc_eval = None
        self.call_stack = None
        self.symbol = None
        self.operation = None
        self.value = None
        self.arguments = None
        self.time_stamp = None

    def __hash__(self):
        a = hashlib.md5(self.script_url.encode())
        b = a.hexdigest()
        as_int = int(b, 16)
        return as_int

    def __eq__(self, other):
        return self.script_url == other.script_url