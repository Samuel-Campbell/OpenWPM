from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.flash_cookies_model import FlashCookiesModel


class FlashCookiesTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
                SELECT         
                flash_cookies.id,
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
                flash_cookies.domain,
                flash_cookies.filename,
                flash_cookies.local_path,
                flash_cookies.key,
                flash_cookies.content
                FROM flash_cookies
                INNER JOIN crawl ON flash_cookies.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON flash_cookies.visit_id = site_visits.visit_id        
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
            flash_cookie_model = FlashCookiesModel()
            flash_cookie_model.id = row[0]
            flash_cookie_model.crawl_id = crawl_model
            flash_cookie_model.visit_id = site_visits_model
            flash_cookie_model.domain = row[14]
            flash_cookie_model.filename = row[15]
            flash_cookie_model.local_path = row[16]
            flash_cookie_model.key = row[17]
            flash_cookie_model.content = row[18]

            model_list.append(flash_cookie_model)
        cursor.close()
        self.disconnect()
        return model_list
