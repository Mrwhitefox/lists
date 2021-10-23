FROM python:3.7-slim

RUN mkdir -p /opt/lists
ADD requirements.txt /opt/lists

RUN pip install -r /opt/lists/requirements.txt

ADD static /opt/lists/static
ADD views /opt/lists/views
ADD lists_http.py conf.yml.dist /opt/lists/


WORKDIR /opt/lists/
EXPOSE 80/tcp
CMD [ "python", "/opt/lists/lists_http.py", "/work/conf.yml" ]
