from tdg.abstract_tdg import AbstractTdg
from models.crawl_history_model import CrawlHistoryModel
from models.task_model import TaskModel
from models.crawl_model import CrawlModel


class CrawlHistoryTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = """
        SELECT         
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
        CrawlHistory.command,
        CrawlHistory.arguments,
        CrawlHistory.bool_success,
        CrawlHistory.dtg
        FROM CrawlHistory
        INNER JOIN crawl ON CrawlHistory.crawl_id = crawl.crawl_id
        INNER JOIN task ON crawl.task_id = task.task_id        
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            # task model
            task_model = TaskModel()
            task_model.task_id = row[1]
            task_model.start_time = row[2]
            task_model.manager_params = row[3]
            task_model.openwpm_version = row[4]
            task_model.browser_version = row[5]

            # crawl model
            crawl_model = CrawlModel()
            crawl_model.crawl_id = row[0]
            crawl_model.task_id = task_model
            crawl_model.browser_params = row[6]
            crawl_model.screen_res = row[7]
            crawl_model.ua_string = row[8]
            crawl_model.finished = row[9]
            crawl_model.start_time = row[10]

            # crawl history model
            crawl_history_model = CrawlHistoryModel()
            crawl_history_model.crawl_id = crawl_model
            crawl_history_model.command = row[11]
            crawl_history_model.arguments = row[12]
            crawl_history_model.bool_success = row[13]
            crawl_history_model.timestamp = row[14]
            model_list.append(crawl_history_model)

        cursor.close()
        self.disconnect()
        return model_list
