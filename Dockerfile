FROM python:3.7

MAINTAINER Brian Schmidt "6666331+schmidtbri@users.noreply.github.com"

COPY ./requirements.txt ./service/requirements.txt

WORKDIR ./service

RUN pip install -r requirements.txt

COPY ./model_websocket_service ./service/model_websocket_service

ENV PYTHONPATH "${PYTHONPATH}:./service"

ENTRYPOINT [ "python" ]

CMD [ "./service/model_websocket_service/service.py" ]