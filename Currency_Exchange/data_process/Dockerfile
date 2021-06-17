# set base image (host OS)
FROM python:3.9.1
ADD /data_process/main.py .
RUN pip install requests pymongo schedule
CMD [ "python", "./main.py" ]