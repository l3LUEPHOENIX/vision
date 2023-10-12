FROM python:3.10
RUN mkdir /opt/vision
COPY . /opt/vision
WORKDIR /opt/vision
RUN pip install -r python_packages/requirements.txt --no-index --find-links python_packages
CMD ["gunicorn","--certfile","cert.pem","--keyfile","key.pem","app:app","--worker-class","gevent", "--bind", "0.0.0.0:7443"]