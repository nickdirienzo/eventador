from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import rfc822

Base = declarative_base()

class Email(Base):
  __tablename__ = 'emails'
  id = Column(Integer, primary_key=True)
  htmlBody = Column(Text)
  textBody = Column(Text)
  domain = Column(Text)
  emailAddress = Column(Text)
  emailAuthor = Column(Text)
  subject = Column(Text)
  eventTime = Column(DateTime)
  eventLocation = Column(Text)

  def __init__(self, htmlBody, textBody, domain, emailAddress, emailAuthor, subject):
    self.htmlBody = htmlBody # email body
    self.textBody = textBody
    self.emailAddress = emailAddress # author's email address
    self.emailAuthor = emailAuthor # author's name i.e. Nick
    self.domain = domain # domain i.e. princeton.edu
    self.subject = subject # subject i.e. "E-Club meeting!"
    self.eventTime = None # event time
    self.eventLocation = None # event location

def parseEmail(messages):
  for message in messages:
    m = Email(message.html.as_string(), 
        message.body.as_string(), 
        message.fr, 
        rfc822.parseaddr(message.fr)[0],
  # -1 gets last element in array
        rfc822.parseaddr(message.fr)[-1].split('@')[-1],
        message.subject)
    print 'Adding message:', message.subject
    db_session.add(m)
  db_session.commit()

# creates engine that stores data in local postgres server		
engine = create_engine('postgresql://janie:yolo@localhost/eventador')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
# creates all tables in engine
  Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
  init_db()

  import eventador_mailbot
  m = eventador_mailbot.Mailbot()
  unread = m.client.inbox().mail(unread=True, prefetch=True)
  parseEmail(unread)
