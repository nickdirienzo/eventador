import flask
from flask.json import JSONEncoder

from models import Email

class EventadorEncoder(JSONEncoder):
  def default(self, obj):
    try:
      if isinstance(obj, Email):
        return obj.to_json()
      iterable = iter(obj)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, obj)

app = flask.Flask(__name__)
app.json_encoder = EventadorEncoder

@app.route('/<string:domain>')
def index(domain):
  domains = Email.query.group_by(Email.domain).with_entities(Email.domain).all()
  return flask.render_template('index.html', domains=domains, selected=domain)

@app.route('/<string:domain>/events')
def events(domain):
  start = flask.request.args.get('start')
  end = flask.request.args.get('end')
  events = []
  #events.append(Event(
  return flask.jsonify(events)

@app.route('/<string:domain>/search')
def search(domain):
  query = flask.request.args.get('query')
  sql_query = '%' + query + '%'
  emails = set([])
  subject_matches = Email.query.filter(Email.subject.like(sql_query)).all()
  for e in subject_matches:
    emails.add(e)
  text_matches = Email.query.filter(Email.text.like(sql_query)).all()
  for e in text_matches:
    emails.add(e)
  return flask.jsonify(emails=emails) 

if __name__ == '__main__':
  app.run(debug=True)
