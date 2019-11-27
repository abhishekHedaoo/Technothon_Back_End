from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin
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
  @cross_origin()
  def getData():
    """
    Example endpoint
    """
    # dataListJson = TNR.getTreeNeeded()
    alldataListJson = DR.getAllDetails()
    return Response(
          mimetype="application/json",
          response=alldataListJson,
          status=200
    )

  @app.route('/process_data', methods=['GET'])
  def processData():
    DR.runDataAnalyticsModule()
    return 200
    
  return app
