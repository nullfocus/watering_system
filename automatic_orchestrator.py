class AutomaticOrchestrator:
    def __init__(self, log, clock, water_device, datastore):
        self.log = log
        self.clock = clock
        self.water_device = water_device
        self.datastore = datastore

    def update(self):
        active_id = self.datastore.get_scheduled_area(*self.clock.get_time())

        self.water_device.turn_on(active_id)

        return active_id

    def get_schedules(self):
        schedules = self.datastore.get_schedules()

        day_of_week, time_of_day = self.clock.get_time()

        active_id = self.datastore.get_scheduled_area(*self.clock.get_time())

        for schedule in schedules:
            if(schedule['areaId'] == active_id):
                schedule['active'] = (schedule['dayOfWeek'] == day_of_week) & (schedule['timeOfDay'] == time_of_day)
            else:
                schedule['active'] = False

        return schedules

    def set_schedule(self, day_of_week, time_of_day, area_id):
        self.datastore.set_schedule(day_of_week, time_of_day, area_id)
