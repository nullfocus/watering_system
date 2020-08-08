from flask import Flask, request, redirect
from functools import wraps
import logging, os

app = Flask(__name__)

active_id = 0

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
                font-family: monospace;
                margin: 0;
                padding: 0;
                border: 0;
                font-size: inherit;
            }}

            html{{ font-size: 60%; padding: 1em;}}
            input, button {{ border: 2px solid #000; padding: .5em; }}

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

            ul{{ list-style: decimal; margin-left: 2em}}
        </style>
    </head>
    <body>
    {content}
    </body>
</html>
'''

def ids_except(id):
    allIds = [1,2,3,4]
    allIds.remove(int(id))

    return allIds

def turn_off(ids):
    #turn off all ids
    log.debug('turning off ' + ' '.join(map(str, ids)))
    return

def turn_on(id):
    #turn on id
    log.debug('turning on ' + str(id))
    return

@app.route('/activate/<id>')
@logged
def activate(id):
    global active_id

    active_id = int(id)

    turn_off(ids_except(active_id))
    turn_on(active_id)

    return redirect('/', code=302)

@app.route('/deactivate/<id>')
@logged
def deactivate(id):
    global active_id

    active_id = 0
    turn_off([1,2,3,4])

    return redirect('/', code=302)

@app.route('/')
@logged
def index():
    global active_id
    content = f'''
<h1>WATERING SYSTEM</h1>
'''

    for id in [1,2,3,4]:
        content += f'''
<div>
    <form action="/{'activate' if id != active_id else 'deactivate'}/{id}">
        <button type="submit">{'Start' if id != active_id else 'Stop'} {id}</button>
    </form>
</div>
'''

    return page('watering system', content)

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
    filepath = os.path.dirname(os.path.realpath(__name__))

    logfile_path = filepath + '/log.txt'

    logging.basicConfig(level=logging.DEBUG, filename=logfile_path)
    log = logging.getLogger(os.path.basename(__file__))
    
    app.run(host='192.168.1.222', debug=True, port=5000)

