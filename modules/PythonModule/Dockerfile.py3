FROM ubuntu:latest

WORKDIR /app

RUN apt-get update \
  && apt-get install -y python3-pip libboost-python1.58.0 libcurl4-openssl-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD [ "python3", "-u", "./main.py" ]
