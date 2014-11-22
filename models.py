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
  htmlBody = Column(Text)
  textBody = Column(CIText)
  domain = Column(Text)
  emailAddress = Column(Text)
  emailAuthor = Column(Text)
  subject = Column(CIText)
  eventTime = Column(DateTime)
  event_end_time = Column(DateTime)
  eventLocation = Column(Text)

  def __init__(self, htmlBody=None, textBody=None, domain=None, emailAddress=None, emailAuthor=None, subject=None):
    self.htmlBody = htmlBody # email body
    self.textBody = textBody
    self.emailAddress = emailAddress # author's email address
    self.emailAuthor = emailAuthor # author's name i.e. Nick
    self.domain = domain # domain i.e. princeton.edu
    self.subject = subject # subject i.e. "E-Club meeting!"
    self.eventTime = None # event time
    self.event_end_time = None
    self.eventLocation = None # event location

  def to_json(self):
    return {'subject': self.subject}

def import_emails(messages):
  for message in messages:
    m = Email(
          htmlBody=message.html.as_string(), 
          textBody=message.body.as_string(), 
          emailAddress=message.fr, 
          emailAuthor=rfc822.parseaddr(message.fr)[0],
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
