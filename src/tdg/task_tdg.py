from tdg.abstract_tdg import AbstractTdg
from models.task_model import TaskModel


class TaskTdg(AbstractTdg):
    def __init__(self):
        AbstractTdg.__init__(self)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = "SELECT * FROM task"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            model = TaskModel()
            model.task_id = row[0]
            model.start_time = row[1]
            model.manager_params = row[2]
            model.openwpm_version = row[3]
            model.browser_version = row[4]
            model_list.append(model)
        cursor.close()
        self.disconnect()
        return model_list
