import flask

import json

app = flask.Flask(__name__)

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/events')
def events():
  start = flask.request.args.get('start')
  end = flask.request.args.get('end')
  events = []
  #events.append(Event(

if __name__ == '__main__':
  app.run(debug=True)
