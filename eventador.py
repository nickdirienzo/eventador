import flask

import json

app = flask.Flask(__name__)

# Replace with actual Event model
class Event(object):
  def __init__(self, start, end, title, id_):
    self.start = start
    self.end = end
    self.title = title
    self.id_ = id_
    self.color = '#66FF33'

  def to_json(self):
    return json.dumps({
      'start': self.start.isoformat(),
      'end': self.end.isoformat(),
      'title': self.title,
      'id': self.id_,
      'color': self.color
    })

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
