FROM python:3.8
COPY requirements.txt ./requirements.txt
ADD . /web-server
WORKDIR /web-server
RUN pip install -r requirements.txt
