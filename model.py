from datetime import datetime
from sqlalchemy import Column, Integer, Text
from sqlalchemy import create_engine
from scqlachemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import rfc822

Base = declarative_base()

class Email(Base)
	__tablename__ = 'parsedEmails'
	htmlBody = Column(Text)
  textBody = Column(Text)
  domain = Column(String(20))
	emailAddress = Column(String(20))
  emailAuthor = Column(String(20))
	subject = Column(String(50))
	eventTime = Column(datetime)
	eventLocation = Column(String(50))
	
	def __init__(htmlBody, textBody, domain, emailAddress, emailAuthor, subject)
		self.htmlBody = htmlBody # email body
    self.textBody = textBody
    self.emailAddress = emailAddress # author's email address
		self.emailAuthor = emailAuthor # author's name i.e. Nick
		self.domain = domain # domain i.e. princeton.edu
    self.subject = subject # subject i.e. "E-Club meeting!"
		self.eventTime = None # event time
		self.eventLocation = None # event location

def parseEmail(messages)
  Session = sessionmaker(bind=engine)
  for message in messages
	  m = Email(message.html.as_string(), 
              message.body.as_string(), 
              message.fr, 
              rfc822.parseaddr(message.fr)[0],
              # -1 gets last element in array
              rfc822.parseaddr(message.fr)[-1].split('@')[-1],
              message.subject)
    session.add(m)
  session.commit()

# creates engine that stores data in local PostSql server		
engine = create_engine('postgresql://hacker@localhost/hacker')

# creates all tables in engine
Base.metadata.create_all(bind=engine)
