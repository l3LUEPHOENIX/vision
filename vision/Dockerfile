FROM python:3.10-alpine
RUN mkdir /opt/vision
COPY . /opt/vision
WORKDIR /opt/vision
RUN pip install python_packages/*
RUN python3 vision_config_gen.py && \
    rm vision_config_gen.py
CMD ["gunicorn","--certfile","cert.pem","--keyfile","key.pem","app:app","--worker-class","gevent", "--bind", "0.0.0.0:7443"]