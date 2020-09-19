import sqlite3 as sql

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DatastoreSqlite:
    def __init__(self, log):
        self.log = log

        with self.con() as con:        
            con.execute('create table if not exists Schedules (dayOfWeek integer NOT NULL, timeOfDay integer NOT NULL, areaId integer NOT NULL, unique(dayofweek, timeofday))')
            con.execute('create table if not exists Areas (areaId integer NOT NULL, name varchar(64) NOT NULL, unique(areaId))')

    def con(self):
        con = sql.connect('data.sqlite3')
        con.row_factory = dict_factory

        return con
 
    def get_areas(self):
        with self.con() as con:
            cur = con.cursor()
            cur.execute('select areaId, name from Areas order by areaId')

            return cur.fetchall()

    def create_area(self, area_id, name):
        with self.con() as con:
            cur = con.cursor()
            cur.execute('insert or replace into Areas (areaId, name) values (?, ?) ', (area_id, name))

    def delete_area(self, area_id):
        with self.con() as con:
            cur = con.cursor()
            cur.execute('delete from Areas where areaId = ?', (area_id))

    def get_scheduled_area(self, day_of_week, time_of_day):
        with self.con() as con:
            cur = con.cursor()
            cur.execute('select areaId from Schedules where dayOfWeek=? and timeOfDay=?', (day_of_week, time_of_day))

            area_row = cur.fetchone()

            if area_row is None:
                return None
            else:
                return area_row['areaId']

    def get_schedules(self):
        with self.con() as con:
            cur = con.cursor()
            cur.execute('select s.dayOfWeek, s.timeOfDay, s.areaId, a.name from Schedules s join Areas a on s.areaID = a.areaId order by s.dayOfWeek, s.timeOfDay')

            return cur.fetchall()

    def set_schedule(self, day_of_week, time_of_day, area_id):
        with self.con() as con:
            cur = con.cursor()

            if area_id is None:
                self.log(f"deleting {day_of_week} {time_of_day}")
                cur.execute('delete from Schedules where dayOfWeek = ? and timeOfDay = ?', (day_of_week, time_of_day))

            else:
                self.log(f"inserting {day_of_week} {time_of_day} {area_id}")
                cur.execute('insert or replace into Schedules (dayOfWeek, timeOfDay, areaId) values (?, ?, ?)', (day_of_week, time_of_day, area_id))