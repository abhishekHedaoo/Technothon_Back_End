# import os
from src.app import create_app
# import src.app as app
# import src

if __name__ == '__main__':
  env_name= 'developement'
  app = create_app(env_name)
  #run app
  app.run()