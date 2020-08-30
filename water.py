from flask import Flask, request, redirect
from functools import wraps
import logging, os
import RPi.GPIO as GPIO

app = Flask(__name__)

ticks_to_ml = 0.00225

gpio_in_counter=0
gpio_out_active_id = 0
gpio_in_pin = 8
gpio_out_pins = [7, 11, 13, 15]

def logged(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        log.debug(f.__name__ + f'({kwargs})')
        return f(*args, **kwargs)
    return decorated

def page(title, content):
    return f'''
<html>
    <head>
        <title>{title}</title>
        <style>
            html, body, div, ul, li, a, input, button {{
                display: grid;
                font-family: monospace;
                margin: 0;
                padding: 0;
                border: 0;
                font-size: inherit;
            }}

            html{{ font-size: 60%; padding: 1em;}}
            input, button {{ border: 2px solid #000; padding: .5em; }}
            ul{{ list-style: decimal; margin-left: 2em}}

            @media screen 
                and (min-width: 0px)
                and (max-width: 300px) 
            {{ html {{ font-size: 4em; }} }}

            @media screen 
                and (min-width: 301px)
                and (max-width: 600px) 
            {{ html {{ font-size: 3.5em; }} }}

            @media screen 
                and (min-width: 601px)
                and (max-width: 1000px) 
            {{ html {{ font-size: 3em; }} }}

            @media screen 
                and (min-width: 1001px)
            {{ html {{ font-size: 2em; }} }}

            body{{
                justify-items: center;
            }}
        </style>
    </head>
    <body>
    {content}
    </body>
</html>
'''

def gpio_in_handler(input):
    global gpio_in_counter
    gpio_in_counter += 1

def turn_off():
    global gpio_out_pins
    
    log.debug('turning off all')
    GPIO.output(gpio_out_pins,GPIO.HIGH)

def turn_on(id):
    global gpio_out_pins
    
    log.debug('turning on ' + str(id))
    GPIO.output(gpio_out_pins[id-1],GPIO.LOW)

@app.route('/activate/<id>')
@logged
def activate(id):
    global gpio_out_active_id, gpio_in_counter

    gpio_out_active_id = int(id)
    gpio_in_counter = 0

    turn_off()
    turn_on(gpio_out_active_id)

    return redirect('/', code=302)

@app.route('/deactivate/<id>')
@logged
def deactivate(id):
    global gpio_out_active_id

    gpio_out_active_id = 0
    turn_off()

    return redirect('/', code=302)

@app.route('/')
@logged
def index():
    global gpio_out_active_id
    content = f'''
<h1>WATERING SYSTEM</h1>
<script>
var is_active = false;
</script>
'''

    for id in [1,2,3,4]:
        id_is_active = (id == gpio_out_active_id)
        
        content += f'''
<div>
    <form action="/{'deactivate' if id_is_active else 'activate'}/{id}">
        <button type="submit">{'Stop' if id_is_active else 'Start'} {id}</button>
    </form>
    <script>
        is_active = {'true' if id_is_active else 'false'};
    </script>
</div>
'''

    content += f'''
<div id="liters">{current_liters()} liters</div>

<script>
var intervalId = -1;
var waterCheckInterval = 3000;//ms
var msDisplayInterval = 32;
var increment = 0;
var curNumber = 0;
var nextNumber = 0;

function setNextNumber(number){{

    if(!is_active){{
        document.getElementById('liters').innerText = number.toFixed(2) + " liters";
        nextNumber = number;
        curNumber = number;
        return;
    }}

    nextNumber = number;
    var increment = ( nextNumber - curNumber) / (waterCheckInterval / msDisplayInterval);
  
    clearInterval(intervalId);
    
    intervalId = setInterval(function(){{
        curNumber += increment;
    
        if(curNumber >= nextNumber){{
            clearInterval(intervalId);
            curNumber = nextNumber;
        }}
        
        
        document.getElementById('liters').innerText = curNumber.toFixed(2) + " liters";
        
    }}, msDisplayInterval);
}}


setInterval(function(){{ 
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function() {{ setNextNumber(parseFloat(this.responseText)) }});
    oReq.open("GET", "/current_liters");
    oReq.send();
}}, waterCheckInterval);

</script>
'''

    return page('watering system', content)

def current_liters():
    global  gpio_in_counter, ticks_to_ml
    return round(gpio_in_counter*ticks_to_ml, 3)

@app.route('/current_liters')
@logged
def get_liters():
    return f'''{current_liters()} liters'''

@app.route('/favicon.ico')
@logged
def favicon():
    return '', 404

#https://blog.sneawo.com/blog/2017/12/20/no-cache-headers-in-flask/
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(Exception)
def all_exception_handler(error):
    log.debug(error)
    return 'Error', 500

if __name__ == '__main__':

    try:
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(gpio_in_pin,GPIO.IN)
        GPIO.add_event_detect(gpio_in_pin, GPIO.RISING, callback=gpio_in_handler)

        GPIO.setup(gpio_out_pins,GPIO.OUT)
        GPIO.output(gpio_out_pins,GPIO.HIGH)
        filepath = os.path.dirname(os.path.realpath(__name__))

        logfile_path = filepath + '/log.txt'

        logging.basicConfig(level=logging.DEBUG, filename=logfile_path)
        log = logging.getLogger(os.path.basename(__file__))
        
        app.run(host='0.0.0.0', debug=True, port=5000)
    finally:
        GPIO.output(gpio_out_pins,GPIO.HIGH)
        GPIO.cleanup()
        

