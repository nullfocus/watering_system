from manual_orchestrator import ManualOrchestrator
from automatic_orchestrator import AutomaticOrchestrator

class Orchestrator:
    def __init__(self, log, clock, water_device, datastore):
        self.log = log
        self.clock = clock
        self.water_device = water_device
        self.datastore = datastore

        self.manual_mode_on = False

        self.manual_orchestrator = ManualOrchestrator(log, water_device, datastore)
        self.automatic_orchestrator = AutomaticOrchestrator(log, clock, water_device, datastore)

    def set_mode(self, mode):
        if(self.manual_mode_on != mode):
            self.manual_orchestrator.deactivate()
            self.water_device.turn_off()

        self.manual_mode_on = mode

        self.update()
    
    def get_mode(self):
        return self.manual_mode_on

    def update(self):
        if(not self.manual_mode_on):
            self.log('automatic mode, doing update')
            self.automatic_orchestrator.update()
        else:
            self.log('manual mode, skipping update')
        
    #========manual mode=====#

    def activate(self, area_id):
        if(self.manual_mode_on):
            self.manual_orchestrator.activate(area_id)

    def deactivate(self):
        if(self.manual_mode_on):
            self.manual_orchestrator.deactivate()

    def area_statuses(self):
        return self.manual_orchestrator.area_statuses()

    #======automatic mode====#

    def get_schedules(self):
        return self.automatic_orchestrator.get_schedules()

    def set_schedule(self, day_of_week, time_of_day, area_id):
        self.automatic_orchestrator.set_schedule(day_of_week, time_of_day, area_id)


    #---------debugging-----------#
    def test(self):
        self.datastore.create_area(0, 'back lawn 2')
        self.datastore.create_area(1, 'back lawn 1')
        self.datastore.create_area(2, 'drip system')
        self.datastore.create_area(3, 'front lawn')
