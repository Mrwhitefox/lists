FROM python:3.7-slim

ADD lists_http.py requirements.txt conf.yml.dist /opt/lists/
ADD static /opt/lists/static
ADD views /opt/lists/views

RUN pip install -r /opt/lists/requirements.txt

WORKDIR /opt/lists/
EXPOSE 80/tcp
CMD [ "python", "/opt/lists/lists_http.py", "/work/conf.yml" ]
