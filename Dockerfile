FROM ubuntu:focal
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    git \
    qemu-utils \
    python3-dev \
    libssl-dev \
    ipmitool \
    python3-pip \
    python3-venv \
    vim \
    curl \
    libev-dev \
    libvirt-dev \
    libffi-dev \
    libyaml-dev \
    lsb-release && \
    apt-get clean all

COPY .teuthology.yaml /root
WORKDIR /teuthology_api
COPY requirements.txt *.env /teuthology_api/
RUN pip3 install -r requirements.txt
COPY . /teuthology_api/

WORKDIR /teuthology_api/src
ENTRYPOINT gunicorn -c /teuthology_api/gunicorn_config.py main:app
