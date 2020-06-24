FROM python:3.6 
#RUN pip install redis
RUN pip install flask
#RUN pip install uwsgi
RUN pip install flask-cors
RUN pip install requests
#RUN pip install ptvsd==3.0.0
#RUN pip install debugpy
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["python3"]

