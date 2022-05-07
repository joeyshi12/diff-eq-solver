FROM ubuntu:20.04

RUN apt-get -y update && \
    apt-get python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    pythons3-wheel

RUN pip install -r requirements.txt && pip install -r requirements_dev.txt

RUN pip install .

EXPOSE 41984

CMD ["detk"]
