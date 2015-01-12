import redis


redis_connection = None

IGNORED_WORDS = ['Hall']

class NoDomainSupplied(Exception):
  pass


class NoLocationSupplied(Exception):
  pass


def init():
  global redis_connection
  redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)    


def load(fp, domain=None):
  if not domain:
      raise NoDomainSupplied("'domain' cannot be Falsey.")

  with open(fp, 'r') as f:
      for line in f.readlines():
          location = line.strip()
          for word in IGNORED_WORDS:
              location = location.rstrip(word)
        
          location = location.strip()
          if not is_location(domain, location):
              add_location(domain, location)


def add_location(domain=None, location=None):
  if not domain:
      raise NoDomainSupplied("'domain' cannot be Falsey.")

  if not location:
      raise NoLcationSupplied("'location' cannot be Falsey.")

  redis_connection.sadd(domain, location)    


def is_location(domain=None, maybe_location=None):
  if not domain:
      raise NoDomainSupplied("'domain' cannot be Falsey.")

  if not maybe_location:
      raise NoLcationSupplied("'location' cannot be Falsey.")

  return redis_connection.sismember(domain, maybe_location)
