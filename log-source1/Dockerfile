FROM python:3.10
RUN mkdir /opt/log-source
COPY . /opt/log-source
WORKDIR /opt/log-source
RUN pip install -r python_packages/requirements.txt --no-index --find-links python_packages
RUN chmod a+x run.sh
CMD ["./run.sh"]