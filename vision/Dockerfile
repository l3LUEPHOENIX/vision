FROM python:3.10-alpine
RUN mkdir /opt/vision
COPY . /opt/vision
WORKDIR /opt/vision
# RUN pip install --no-index --find-links pyhton_packages/ wheel
RUN pip install --no-index --no-build-isolation --find-links python_packages/ python_packages/*
CMD ["gunicorn","--certfile","./secrets/cert.pem","--keyfile","./secrets/key.pem","app:app","--worker-class","gevent", "--bind", "0.0.0.0:7443"]