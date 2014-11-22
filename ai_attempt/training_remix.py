with open('event.tsv', 'r') as tsv:
  with open('event2.tsv', 'w') as tsv2:
    for line in tsv.readlines():
      if line.split()[-1] == 'O':
        tsv2.write(line.split()[0] + '\n')
      else:
        tsv2.write(line)
