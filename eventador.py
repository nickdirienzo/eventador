import flask
from flask.json import JSONEncoder

from models import Email

class EventadorEncoder(JSONEncoder):
  def default(self, o):
    try:
      if isinstance(o, Email):
        return o.to_json()
      iterable = iter(o)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, o)

app = flask.Flask(__name__)
app.json_encoder = EventadorEncoder

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/events')
def events():
  start = flask.request.args.get('start')
  end = flask.request.args.get('end')
  events = []
  #events.append(Event(
  return flask.jsonify(events)

@app.route('/search')
def search():
  query = flask.request.args.get('query')
  sql_query = '%' + query + '%'
  print sql_query
  emails = set([])
  subject_matches = Email.query.filter(Email.subject.like(sql_query)).all()
  for e in subject_matches:
    emails.add(e)
  text_matches = Email.query.filter(Email.textBody.like(sql_query)).all()
  for e in text_matches:
    emails.add(e)
  return flask.jsonify(emails=emails) 


if __name__ == '__main__':
  app.run(debug=True)
