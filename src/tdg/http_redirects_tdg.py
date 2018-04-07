from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.http_redirects_model import HttpRedirectsModel


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
                http_redirects.old_channel_id,
                http_redirects.new_channel_id,
                http_redirects.is_temporary,
                http_redirects.is_permanent,
                http_redirects.is_internal,
                http_redirects.is_sts_upgrade,
                http_redirects.time_stamp
                FROM http_redirects
                INNER JOIN crawl ON http_redirects.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON http_redirects.visit_id = site_visits.visit_id        
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
            http_redirects_model = HttpRedirectsModel()
            http_redirects_model.id = row[0]
            http_redirects_model.crawl_id = crawl_model
            http_redirects_model.visit_id = site_visits_model
            http_redirects_model.old_channel_id = row[14]
            http_redirects_model.new_channel_id = row[15]
            http_redirects_model.is_temporary = row[16]
            http_redirects_model.is_permanent = row[17]
            http_redirects_model.is_internal = row[18]
            http_redirects_model.is_sts_upgrade = row[19]
            http_redirects_model.time_stamp = row[20]

            model_list.append(http_redirects_model)
        cursor.close()
        self.disconnect()
        return model_list
