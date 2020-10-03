from flask import Flask, request, jsonify, redirect, send_from_directory

app = Flask(__name__)

log = None
orchestrator = None

def start(l, o):
    global log, orchestrator
    log = l
    orchestrator = o
    app.run(host='0.0.0.0', debug=False, port=5000)

#---api section---

@app.route('/test/')
def test():
    global orchestrator
    orchestrator.test()
    return redirect('/status/')

@app.route('/status/')
def status():
    global orchestrator

    return jsonify(
        manualMode = orchestrator.get_mode(),
        wateringAreas = orchestrator.area_statuses(),
        wateringSchedules = orchestrator.get_schedules()
    )

@app.route('/set_manual_mode/')
def set_manual_mode():
    global orchestrator
        
    orchestrator.set_mode(True)
    return status()

@app.route('/set_automatic_mode/')
def set_automatic_mode():
    global orchestrator
        
    orchestrator.set_mode(False)
    return status()
    
@app.route('/activate/<area_id>')
def activate(area_id):
    global orchestrator
    orchestrator.activate(area_id)
    return status()

@app.route('/deactivate/')
def deactivate():
    global orchestrator
    orchestrator.deactivate()
    return status()

@app.route('/set_active/<day_of_week>/<time_of_day>/<area>')
def set_active(day_of_week, time_of_day, area):
    global orchestrator
    
    if area == 'null': 
        area = None
        
    id = orchestrator.set_active(day_of_week, time_of_day, area)
    return jsonify(success = True, active_id = id)

#---static file section---

@app.route('/')
def root_redirect():
    return redirect('/status/')

@app.errorhandler(Exception)
def all_exception_handler(error):
    return '<html><body><h1>Exception</h1><br/><h3>' + error + '</h3><br/>' + error.description + '</body></html>', 500

@app.route('/favicon.ico')
def favicon():
    return '', 404

#https://blog.sneawo.com/blog/2017/12/20/no-cache-headers-in-flask/
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

