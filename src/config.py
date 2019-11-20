class Develpoment:
  """
  Development environment configuration
  """
  DEBUG = True
  TESTING = False

class Production:
  """
  Production environment cofiguration
  """
  DEBUG = False
  TESTING = False

app_config = {
  'developement': Develpoment,
  'production': Production,
}
