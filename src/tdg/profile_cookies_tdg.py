from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.profile_cookies_model import ProfileCookiesModel


class ProfileCookiesTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
                SELECT         
                profile_cookies.id,
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
                profile_cookies.baseDomain,
                profile_cookies.name,
                profile_cookies.value,
                profile_cookies.host,
                profile_cookies.path,
                profile_cookies.expiry,
                profile_cookies.accessed,
                profile_cookies.creationTime,
                profile_cookies.isSecure,
                profile_cookies.isHttpOnly
                FROM profile_cookies
                INNER JOIN crawl ON profile_cookies.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON profile_cookies.visit_id = site_visits.visit_id        
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
            profile_cookies_model = ProfileCookiesModel()
            profile_cookies_model.id = row[0]
            profile_cookies_model.crawl_id = crawl_model
            profile_cookies_model.visit_id = site_visits_model
            profile_cookies_model.baseDomain = row[14]
            profile_cookies_model.name = row[15]
            profile_cookies_model.value = row[16]
            profile_cookies_model.host = row[17]
            profile_cookies_model.path = row[18]
            profile_cookies_model.expiry = row[19]
            profile_cookies_model.accessed = row[20]
            profile_cookies_model.creationTime = row[21]
            profile_cookies_model.isSecure = row[22]
            profile_cookies_model.isHttpOnly = row[23]

            model_list.append(profile_cookies_model)
        cursor.close()
        self.disconnect()
        return model_list
