from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.http_responses_model import HttpResponsesModel


class HttpResponsesTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
                SELECT         
                http_responses.id,
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
                http_responses.content_hash
                FROM http_responses
                INNER JOIN crawl ON http_responses.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON http_responses.visit_id = site_visits.visit_id        
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

            # flash cookie model
            http_responses_model = HttpResponsesModel()
            http_responses_model.id = row[0]
            http_responses_model.crawl_id = crawl_model
            http_responses_model.visit_id = site_visits_model
            http_responses_model.url = row[14]
            http_responses_model.method = row[15]
            http_responses_model.referrer = row[16]
            http_responses_model.response_status = row[17]
            http_responses_model.response_status_text = row[18]
            http_responses_model.is_cached = row[19]
            http_responses_model.headers = row[20]
            http_responses_model.channel_id = row[21]
            http_responses_model.location = row[22]
            http_responses_model.time_stamp = row[23]
            http_responses_model.content_hash = row[24]

            model_list.append(http_responses_model)
        cursor.close()
        self.disconnect()
        return model_list
