import gmail_client

import os
import time
import threading

USER = 'EVENTADOR_USER'
PASS = 'EVENTADOR_PASS'

TIME_TO_CHECK = 10 * 60  # Check every ten minutes...

class Mailbot(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.client = gmail_client.login(os.environ.get(USER), os.environ.get(PASS))

  def process_inbox(self):
    unread = self.client.inbox().mail(unread=True, prefetch=True)
    import pdb
    pdb.set_trace()

  def run(self):
    while True:
      self.process_inbox()
      time.sleep(TIME_TO_CHECK)

if __name__ == '__main__':
  Mailbot().start()
