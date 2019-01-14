import sqlite3


class Sqlite:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db, timeout=5)
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        finally:
            self.close_conn()

    def update_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        finally:
            self.close_conn()

    def query_data(self, sql):

        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            pass
        finally:
            self.close_conn()
        return results

    def close_conn(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def store_csv(self, sql, data):
        """store data into database with given sql"""
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        finally:
            self.close_conn()

if __name__ == '__main__':
    import os

    address = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/'
    sqlite = Sqlite(address + 'ip.db')

    # sqlite.create_table(
    #     'create table ip_house(id INT,proxy_adress TEXT,flag TEXT)')
    # # # sqlite.cursor.execute('''DELETE FROM ftx_house''')
    # sqlite.cursor.execute('''drop table ftx_house''')
    # sqlite.conn.commit()
    print(sqlite.query_data('select proxy_adress from ip_house'))
    # with open('/home/wenhuanhuan/Downloads/sales_part_tab(new).csv') as f:
    #     reader = csv.reader(f)
    #     for field in reader:
    #         sqlite.cursor.execute("INSERT INTO demo VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", field)
    # sqlite.conn.commit()
    # results = results = sqlite.query_data(
    #         'select distinct prod_des,page_width,page_height,size from demo where instr(description, "' + product + '") > 0 or instr(catalog_desc, "' + product + '") > 0')
    # resp = {}
    # for result in results:
    #     if resp.get(result[3]) is None:
    #         resp[result[3]] = [[result[0],result[1],result[2]]]
    #     else:
    #         resp[result[3]].append([result[0],result[1],result[2]])
    # for k,v in resp.items():
    #     page = ''
    #     flag = False
    #     for c in v:
    #         if not flag:
    #             flag = True
    #         else:
    #             page += '; '
    #         page = page+c[0]+':'+c[1]+'*'+c[2]+'mm'
    #     print(k+': '+page+'\n')
    # sqlite.close_conn()

