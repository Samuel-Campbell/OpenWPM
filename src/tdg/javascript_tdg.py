from tdg.abstract_tdg import AbstractTdg
from models.site_visits_model import SiteVisitsModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel
from models.javascript_model import JavascriptModel


class JavascriptTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
                SELECT         
                javascript.id,
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
                javascript.script_url,
                javascript.script_line,
                javascript.script_col,
                javascript.func_name,
                javascript.script_loc_eval,
                javascript.call_stack,
                javascript.symbol,
                javascript.operation,
                javascript.value,
                javascript.arguments,
                javascript.time_stamp
                FROM javascript
                INNER JOIN crawl ON javascript.crawl_id = crawl.crawl_id
                INNER JOIN task ON crawl.task_id = task.task_id
                INNER JOIN site_visits ON javascript.visit_id = site_visits.visit_id        
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
            javascript_model = JavascriptModel()
            javascript_model.id = row[0]
            javascript_model.crawl_id = crawl_model
            javascript_model.visit_id = site_visits_model
            javascript_model.script_url = row[14]
            javascript_model.script_line = row[15]
            javascript_model.script_col = row[16]
            javascript_model.func_name = row[17]
            javascript_model.script_loc_eval = row[18]
            javascript_model.call_stack = row[19]
            javascript_model.symbol = row[20]
            javascript_model.operation = row[21]
            javascript_model.value = row[22]
            javascript_model.arguments = row[23]
            javascript_model.time_stamp = row[24]

            model_list.append(javascript_model)
        cursor.close()
        self.disconnect()
        return model_list
