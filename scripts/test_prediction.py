import socketio


sio = socketio.Client()


def main():
    sio.connect('http://0.0.0.0:80')
    data = {'model_qualified_name': 'iris_model',
            'input_data': {'sepal_length': 1.1, 'sepal_width': 1.1, 'petal_length': 1.1, 'petal_width': 1.1}}
    sio.emit('prediction_request', data)


@sio.on('prediction_response')
def on_message(data):
    print('Prediction response: {}'.format(str(data)))


@sio.on('prediction_error')
def on_message(data):
    print('Prediction error: {}'.format(str(data)))


if __name__ == "__main__":
    main()
