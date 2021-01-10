FROM python:3.8.1
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /home/project/workspace/SmartEvent
WORKDIR /home/project/workspace/SmartEvent

COPY requirements/ requirements/

RUN pip install -r requirements/development.txt

# EXPOSE 5432