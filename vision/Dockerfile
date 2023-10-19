FROM python:3.10-alpine
RUN mkdir /opt/vision
COPY . /opt/vision
WORKDIR /opt/vision
RUN pip install python_packages/*
CMD ["gunicorn","--certfile","./secrets/cert.pem","--keyfile","./secrets/key.pem","app:app","--worker-class","gevent", "--bind", "0.0.0.0:7443"]