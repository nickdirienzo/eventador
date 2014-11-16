import re
import rfc822

import eventador_mailbot

with open('buffalo_training.tsv', 'a') as buffalo_tsv:
  with open('princeton_training.tsv', 'a') as pton_tsv:
    m = eventador_mailbot.Mailbot()
    unread = m.get_unread()
    num_unread = len(unread)
    for i, e in enumerate(unread):
      print 'Processing %s/%s...' % (i + 1, num_unread)
      domain = rfc822.parseaddr(e.fr)[-1].split('@')[-1]
      message = e.body.get_payload()
      tokens = re.findall(r"[\w']+|[-@.,!?;()_]", message)
      default_data = ['%s O' % token for token in tokens]
      to_write = '\n'.join(default_data) + '\n'
      if 'princeton' in domain:
        pton_tsv.write(to_write)
      elif 'buffalo' in domain:
        buffalo_tsv.write(to_write)
      
