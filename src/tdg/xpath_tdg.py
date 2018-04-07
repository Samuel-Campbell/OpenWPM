from tdg.abstract_tdg import AbstractTdg
from models.xpath_model import XpathModel


class XpathTdg(AbstractTdg):
    def __init__(self, database):
        AbstractTdg.__init__(self, database)

    def select(self):
        model_list = []
        self.connect()
        cursor = self.connection.cursor()
        query = "SELECT * FROM xpath"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            model = XpathModel()
            model.id = row[0]
            model.name = row[1]
            model.url = row[2]
            model.xpath = row[3]
            model.absolute_xpath = row[4]
            model.ctime = row[5]
            model_list.append(model)
        cursor.close()
        self.disconnect()
        return model_list
