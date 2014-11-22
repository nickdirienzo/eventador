import gmail_client

import re
import rfc822
import os
import time
import threading

import models

USER = 'EVENTADOR_USER'
PASS = 'EVENTADOR_PASS'

TIME_TO_CHECK = 10 * 60  # Check every ten minutes...

class Mailbot(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.client = gmail_client.login(os.environ.get(USER), os.environ.get(PASS))

  def get_unread(self):
    return self.client.inbox().mail(unread=True, prefetch=True)

  def process_inbox(self):
    unread = self.get_unread()
    models.import_emails(unread)
    for u in unread:
      u.mark_read()

  def run(self):
    print 'Starting mailbot...'
    while True:
      self.process_inbox()
      print 'Sleeping for %s seconds...' % TIME_TO_CHECK
      time.sleep(TIME_TO_CHECK)

if __name__ == '__main__':
  Mailbot().run()
