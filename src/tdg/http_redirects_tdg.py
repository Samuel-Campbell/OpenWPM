from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.http_redirects_model import HttpRedirectsModel
from models.http_responses_model import HttpResponsesModel
from models.http_requests_model import HttpRequestsModel


class HttpRedirectsTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
                SELECT         
                http_redirects.id,
                crawl.crawl_id,
                task.task_id,
                task.start_time,
                task.manager_params,
                task.openwpm_version,
                task.browser_version,
                crawl.browser_params,
                crawl.screen_res,
                crawl.ua_string,
                crawl.finished,
                crawl.start_time,
                site_visits.visit_id,
                site_visits.site_url,
                http_requests.id,
                http_requests.url,
                http_requests.top_level_url,
                http_requests.method,
                http_requests.referrer,
                http_requests.headers,
                http_requests.channel_id,
                http_requests.is_XHR,
                http_requests.is_frame_load,
                http_requests.is_full_page,
                http_requests.is_third_party_channel,
                http_requests.is_third_party_window,
                http_requests.triggering_origin,
                http_requests.loading_origin,
                http_requests.loading_href,
                http_requests.req_call_stack,
                http_requests.content_policy_type,
                http_requests.post_body,
                http_requests.time_stamp,
                http_responses.id,
                http_responses.url,
                http_responses.method,
                http_responses.referrer,
                http_responses.response_status,
                http_responses.response_status_text,
                http_responses.is_cached,
                http_responses.headers,
                http_responses.channel_id,
                http_responses.location,
                http_responses.time_stamp,
                http_responses.content_hash,
                http_redirects.is_temporary,
                http_redirects.is_permanent,
                http_redirects.is_internal,
                http_redirects.is_sts_upgrade,
                http_redirects.time_stamp
                FROM http_redirects
                INNER JOIN crawl ON http_redirects.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON http_redirects.visit_id = site_visits.visit_id
                INNER JOIN http_responses ON http_redirects.new_channel_id = http_responses.channel_id
                INNER JOIN http_requests ON http_redirects.old_channel_id = http_requests.channel_id        
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            # task model
            task_model = TaskModel()
            task_model.task_id = row[2]
            task_model.start_time = row[3]
            task_model.manager_params = row[4]
            task_model.openwpm_version = row[5]
            task_model.browser_version = row[6]

            # crawl model
            crawl_model = CrawlModel()
            crawl_model.crawl_id = row[1]
            crawl_model.task_id = task_model
            crawl_model.browser_params = row[7]
            crawl_model.screen_res = row[8]
            crawl_model.ua_string = row[9]
            crawl_model.finished = row[10]
            crawl_model.start_time = row[11]

            # site visits model
            site_visits_model = SiteVisitsModel()
            site_visits_model.visit_id = row[12]
            site_visits_model.crawl_id = crawl_model
            site_visits_model.site_url = row[13]

            # http request model
            http_requests_model = HttpRequestsModel()
            http_requests_model.id = row[14]
            http_requests_model.crawl_id = crawl_model
            http_requests_model.visit_id = site_visits_model
            http_requests_model.url = row[15]
            http_requests_model.top_level_url = row[16]
            http_requests_model.method = row[17]
            http_requests_model.referrer = row[18]
            http_requests_model.headers = row[19]
            http_requests_model.channel_id = row[20]
            http_requests_model.is_XHR = row[21]
            http_requests_model.is_frame_load = row[22]
            http_requests_model.is_full_page = row[23]
            http_requests_model.is_third_party_channel = row[24]
            http_requests_model.is_third_party_window = row[25]
            http_requests_model.triggering_origin = row[26]
            http_requests_model.loading_origin = row[27]
            http_requests_model.loading_href = row[28]
            http_requests_model.req_call_stack = row[29]
            http_requests_model.content_policy_type = row[30]
            http_requests_model.post_body = row[31]
            http_requests_model.time_stamp = row[32]

            # http response model
            http_responses_model = HttpResponsesModel()
            http_responses_model.id = row[33]
            http_responses_model.crawl_id = crawl_model
            http_responses_model.visit_id = site_visits_model
            http_responses_model.url = row[34]
            http_responses_model.method = row[35]
            http_responses_model.referrer = row[36]
            http_responses_model.response_status = row[37]
            http_responses_model.response_status_text = row[38]
            http_responses_model.is_cached = row[39]
            http_responses_model.headers = row[40]
            http_responses_model.channel_id = row[41]
            http_responses_model.location = row[42]
            http_responses_model.time_stamp = row[43]
            http_responses_model.content_hash = row[44]

            # redirects model
            http_redirects_model = HttpRedirectsModel()
            http_redirects_model.id = row[0]
            http_redirects_model.crawl_id = crawl_model
            http_redirects_model.visit_id = site_visits_model
            http_redirects_model.old_channel_id = http_requests_model
            http_redirects_model.new_channel_id = http_responses_model
            http_redirects_model.is_temporary = row[45]
            http_redirects_model.is_permanent = row[46]
            http_redirects_model.is_internal = row[47]
            http_redirects_model.is_sts_upgrade = row[48]
            http_redirects_model.time_stamp = row[49]

            model_list.append(http_redirects_model)
        cursor.close()
        self.disconnect()
        return model_list
