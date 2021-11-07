FROM python:3.8
COPY requirements.txt ./requirements.txt
ADD . /scanner
WORKDIR /scanner
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y install nmap
