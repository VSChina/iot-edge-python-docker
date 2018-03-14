FROM ubuntu:xenial

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python python-pip python-dev
RUN apt-get install -y libboost1.58-all-dev
RUN apt-get install -y libcurl4-openssl-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u", "./filter.py" ]