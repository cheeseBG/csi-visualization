from sqlalchemy import create_engine

class tracking_db:
    db_user = 'tracking'
    db_pw = ''
    db_host = 'localhost'
    db_name = 'tracking'

    def __init__(self):
        self.engine = create_engine(
            "mysql+mysqldb://" + self.db_user + ":" + self.db_pw + "@" + self.db_host + "/" + self.db_name,
            encoding='utf-8')
        self.conn = self.engine.connect()

    def insert_csi(self, csi_df):
        csi_df.to_sql(name='csi', con=self.engine, if_exists='append', index=False)
