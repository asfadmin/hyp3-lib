FROM ubuntu:16.04

ENV MAPREADY_VERSION=ASF_MapReady

LABEL maintainer="Alaska Satellite Facility" \
    ubuntu_version=16.04 \
    mapready_version=${MAPREADY_VERSION}

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:ubuntugis/ppa

RUN apt-get update && \
    apt-get install -y \
    awscli \
    curl \
    gdal-bin \
    git \
    imagemagick \
    libgeotiff-dev \
    libfftw3-bin \
    libfftw3-dev \
    libgdal-dev \
    libgsl-dev \
    libmotif-dev \
    libshp-dev \
    libx11-dev \
    openssh-client \
    python \
    python-boto3 \
    python-gdal \
    python-lxml \
    python-numpy \
    python-psycopg2 \
    python-pip \
    python-requests \
    python-scipy \
    python3 \
    python3-pip \
    python3-gdal \
    tcsh \
    tree \
    unzip \
    wget \
    xsltproc \
    zip && \
    apt-get update && \
    pip install --upgrade pip

RUN mkdir -p /root/.ssh
ADD ./configs/id_rsa_docker /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config

COPY ./configs/dot.bash_path /root/bash_path
#RUN touch `echo random.$RANDOM`.txt
COPY ./configs/aws_configure.txt /root
RUN aws configure < /root/aws_configure.txt && rm -f /root/aws_configure.txt 
#RUN rm random.*.txt
COPY ./configs/dot.netrc /root/.netrc

WORKDIR /usr/local
RUN git clone git@github.com:asfadmin/gap_rtc.git
RUN git clone git@github.com:asfadmin/python_data_utils.git
RUN git clone git@github.com:asfadmin/cloud-proj.git
RUN git clone git@github.com:asfadmin/asf_api_assistant.git
RUN git clone git@github.com:asfadmin/python-asf.git
RUN git clone git@github.com:asfadmin/change_detection.git
RUN git clone git@github.com:asfadmin/apd_insar.git
RUN git clone git@github.com:asfadmin/hyp3-rtc-gamma.git
RUN git clone git@github.com:asfadmin/hyp3-insar-gamma.git
RUN git clone git@github.com:asfadmin/hyp3-lib.git
RUN git clone git@github.com:asfadmin/hyp3-change-detection-sacd.git

RUN mkdir ./cloud-proj/processing/config/ ./cloud-proj/processing/log ./cloud-proj/processing/lock

# Config stuff starts here
COPY ./configs/get_dem.pl.cfg ./gap_rtc/config/get_dem.pl.cfg
COPY ./configs/sentinel_xml.xsl ./gap_rtc/etc/sentinel_xml.xsl

RUN mkdir ./asf_api_assistant/config/
COPY ./configs/get_asf.cfg ./asf_api_assistant/config/get_asf.cfg

WORKDIR /
RUN mkdir -p /data/hyp3-workdir/attachments

# MapReady
ADD ./lib/${MAPREADY_VERSION}.tar.gz /tmp
RUN cd /tmp/${MAPREADY_VERSION} && make install
RUN rm -rf /tmp
