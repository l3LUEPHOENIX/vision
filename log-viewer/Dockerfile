FROM python:3.10
RUN mkdir /opt/log-viewer
COPY . /opt/log-viewer
WORKDIR /opt/log-viewer
RUN apt-get update -y && \
    apt-get install python3 -y && \
    apt-get install pip -y && \
    apt-get install gunicorn -y && \
    apt-get install python3-gevent -y && \
    pip3 install -r python_packages/requirements.txt --no-index --find-links python_packages
CMD ["python3","app.py"]