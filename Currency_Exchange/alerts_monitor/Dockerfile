FROM python:3.9.1
ADD /alerts_monitor/main.py .
RUN pip install requests pymongo schedule
CMD [ "python", "./main.py" ]