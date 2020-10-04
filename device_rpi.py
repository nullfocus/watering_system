import RPi.GPIO as GPIO

TICKS_TO_ML = 0.00225
GPIO_IN_PIN = 8
GPIO_OUT_PINS = [7, 11, 13, 15]

class DeviceRpi:
    def __init__(self, log):
        self.log = log

        self.gpio_in_counter=0
        self.gpio_out_active_id = 0

        GPIO.setmode(GPIO.BOARD)

        #set up input handler for flow meter
        GPIO.setup(GPIO_IN_PIN, GPIO.IN)
        GPIO.add_event_detect(GPIO_IN_PIN, GPIO.RISING, callback=self.gpio_in_handler)

        #set up output for valves
        GPIO.setup(GPIO_OUT_PINS, GPIO.OUT)
        GPIO.output(GPIO_OUT_PINS, GPIO.HIGH)

    def __del__(self):
        #clean up gpio nicely
        GPIO.output(GPIO_OUT_PINS, GPIO.HIGH)
        GPIO.cleanup()

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
        GPIO.output(GPIO_OUT_PINS, GPIO.HIGH)

    def turn_on(self, id):
        if id == self.gpio_out_active_id:
            self.log(f"id {id} already set")
            return self.gpio_out_active_id

        self.turn_off()

        self.gpio_out_active_id = id

        if id is not None:
            self.log(f"turning on {id}")
            GPIO.output(GPIO_OUT_PINS[int(id)], GPIO.LOW)

        return self.gpio_out_active_id
