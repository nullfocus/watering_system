TICKS_TO_ML = 0.00225

class DeviceStub:
    def __init__(self, log):
        self.log = log
        self.gpio_in_counter=0
        self.gpio_out_active_id = None
    
    def gpio_in_handler(self, input):
        self.gpio_in_counter += 1
    
    def current_liters(self):
        return round(self.gpio_in_counter * TICKS_TO_ML, 3)

    def turn_off(self):
        self.log('turning off')

        if self.gpio_out_active_id == None:
            self.log(f"already turned off")
            return self.gpio_out_active_id

        self.gpio_out_active_id = None
    
    def turn_on(self, id):
        #id is already on, nothing to do
        if id == self.gpio_out_active_id:
            self.log(f"id {id} already set")
            return self.gpio_out_active_id

        #something to do, turn everything off
        self.turn_off()

        #update the active_id
        self.gpio_out_active_id = id

        #if None was passed, just return
        if id is None:
            self.log(f"staying off")
            return self.gpio_out_active_id

        self.log(f"turning on id {id}")

        return self.gpio_out_active_id