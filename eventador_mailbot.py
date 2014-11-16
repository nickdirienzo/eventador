import gmail_client

import re
import rfc822
import os
import time
import threading

USER = 'EVENTADOR_USER'
PASS = 'EVENTADOR_PASS'

TIME_TO_CHECK = 10 * 60  # Check every ten minutes...

class Mailbot(object):

  def __init__(self):
    self.client = gmail_client.login(os.environ.get(USER), os.environ.get(PASS))

  def get_unread(self):
    return self.client.inbox().mail(unread=True, prefetch=True)

  def process_inbox(self):
    unread = self.client.inbox().mail(unread=True, prefetch=True)
    import pdb
    pdb.set_trace()

  def run(self):
    while True:
      self.process_inbox()
      time.sleep(TIME_TO_CHECK)

if __name__ == '__main__':
  unread = Mailbot().get_unread()
  unread = unread[-12::]
  with open('test4.tsv', 'w') as tsv:
    for u in unread:
        domain = rfc822.parseaddr(u.fr)[-1].split('@')[-1]
        message = u.body.get_payload()
        tokens = re.findall(r"[\w']+|[-@.,!?;()_]", message)
        default_data = ['%s O' % token for token in tokens]
        to_write = '\n'.join(default_data) + '\n'
        tsv.write(to_write)
