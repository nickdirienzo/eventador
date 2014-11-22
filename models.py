from datetime import datetime
import rfc822

from citext import CIText
from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# creates engine that stores data in local postgres server		
engine = create_engine('postgresql://janie:yolo@localhost/eventador')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# Allow querying on models directly
Base.query = db_session.query_property()

class Email(Base):
  __tablename__ = 'emails'

  id = Column(Integer, primary_key=True)
  html = Column(Text)
  text = Column(CIText)
  domain = Column(Text)
  author_address = Column(Text)
  author_name = Column(Text)
  subject = Column(CIText)
  start_time = Column(DateTime)
  end_time = Column(DateTime)
  location = Column(Text)

  def __init__(self, html=None, text=None, domain=None, author_address=None, author_name=None, subject=None):
    self.html = htmlBody # email body
    self.text = textBody
    self.author_address = emailAddress # author's email address
    self.author_name = emailAuthor # author's name i.e. Nick
    self.domain = domain # domain i.e. princeton.edu
    self.subject = subject # subject i.e. "E-Club meeting!"
    self.start_time = None # event time
    self.end_time = None
    self.location = None # event location

  def to_json(self):
    return {
      'id': self.id,
      'html': self.html,
      'text': self.text,
      'subject': self.subject,
      'event_start_time': self.start_time,
      'event_end_time': self.end_time,
      'location': self.location
    }

def import_emails(messages):
  for message in messages:
    m = Email(
          html=message.html.as_string(), 
          text=message.body.as_string(), 
          author_address=message.fr, 
          author_name=rfc822.parseaddr(message.fr)[0],
          # -1 gets last element in array
          domain=rfc822.parseaddr(message.fr)[-1].split('@')[-1],
          subject=message.subject
        )
    print 'Adding message:', message.subject
    db_session.add(m)
  db_session.commit()

def init_db():
  # creates all tables in engine
  Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
  pass
#  init_db()
#
#  import eventador_mailbot
#  m = eventador_mailbot.Mailbot()
#  unread = m.client.inbox().mail(unread=True, prefetch=True)
#  parseEmail(unread)
