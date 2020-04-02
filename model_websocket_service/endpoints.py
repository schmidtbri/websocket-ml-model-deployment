"""REST endpoints for the websocket service."""
import logging
from flask import Response
from flask_socketio import emit
from marshmallow.exceptions import ValidationError
from ml_model_abc import MLModelSchemaValidationException

from model_websocket_service import app, socketio
from model_websocket_service.model_manager import ModelManager
from model_websocket_service.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorResponseSchema, \
    PredictionRequest, PredictionResponse

model_collection_schema = ModelCollectionSchema()
model_metadata_schema = ModelMetadataSchema()
error_response_schema = ErrorResponseSchema()
prediction_request_schema = PredictionRequest()
prediction_response_schema = PredictionResponse()

logger = logging.getLogger(__name__)


@app.route("/api/models", methods=['GET'])
def get_models():
    """List of models.

    ---
    get:
      responses:
        200:
          description: List of model available
          content:
            application/json:
              schema: ModelCollectionSchema
    """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()
    response_data = model_collection_schema.dumps(dict(models=models))
    return response_data, 200


@app.route("/api/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """Metadata about one model.

    ---
    get:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model for which metadata is being requested.
      responses:
        200:
          description: Metadata about one model
          content:
            application/json:
              schema: ModelMetadataSchema
        404:
          description: Model not found.
          content:
            application/json:
              schema: ErrorSchema
    """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)
    if metadata is not None:
        response_data = model_metadata_schema.dumps(metadata)
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_response_schema.dumps(response)
        return Response(response_data, status=400, mimetype='application/json')


@socketio.on('prediction_request')
def message(message):
    """Handle a prediction request message."""
    # attempting to deserialize JSON
    try:
        data = prediction_request_schema.load(message)
    except ValidationError as e:
        response_data = dict(type="DESERIALIZATION_ERROR", message=str(e))
        response = error_response_schema.load(response_data)
        emit('prediction_error', response)
        return

    # getting the model object from the Model Manager
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=data["model_qualified_name"])

    # returning an error if model is not found
    if model_object is None:
        response_data = dict(model_qualified_name=data["model_qualified_name"],
                             type="ERROR", message="Model not found.")
        response = error_response_schema.load(response_data)
        emit('prediction_error', response)
    else:
        try:
            prediction = model_object.predict(data["input_data"])
            response_data = dict(model_qualified_name=model_object.qualified_name,
                                 prediction=prediction)
            response = prediction_response_schema.load(response_data)
            emit('prediction_response', response)
        except MLModelSchemaValidationException as e:
            # responding with an error if the schema does not meet the model's input schema
            response_data = dict(model_qualified_name=model_object.qualified_name,
                                 type="SCHEMA_ERROR", message=str(e))
            response = error_response_schema.load(response_data)
            emit('prediction_error', response)
        except Exception as e:
            response_data = dict(model_qualified_name=model_object.qualified_name,
                                 type="ERROR", message="Could not make a prediction.")
            response = error_response_schema.load(response_data)
            emit('prediction_error', response)


@socketio.on('connect')
def connect():
    """Handle a websocket connect event."""
    logger.info("Connected")


@socketio.on('disconnect')
def disconnect():
    """Handle a websocket disconnect event."""
    logger.info('Disconnect')
