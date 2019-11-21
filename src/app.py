from flask import Flask, Response, jsonify
import json
import resource.TreeNeededResources as TNR
import resource.DetailsResources as DR

from .config import app_config

def create_app(env_name):
  """
  Create app
  """

  #app initialization
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  @app.route('/', methods=['GET'])
  def getData():
    """
    Example endpoint
    """
    # dataListJson = TNR.getTreeNeeded()
    alldataListJson = DR.getAllDetails()
    return alldataListJson, 200

  return app
