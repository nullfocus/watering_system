class ManualOrchestrator:
    def __init__(self, log, water_device, datastore):
        self.log = log
        self.water_device = water_device
        self.datastore = datastore
        self.active_area_id = None

    def activate(self, area_id):
        self.active_area_id = area_id
        self.water_device.turn_on(area_id)

    def deactivate(self):
        self.active_area_id = None
        self.water_device.turn_off()

    def area_statuses(self):
        areas = self.datastore.get_areas()

        for area in areas:
            if(str(area['areaId']) == str(self.active_area_id)):
                area['active'] = True
            else:
                area['active'] = False
                
        return areas
