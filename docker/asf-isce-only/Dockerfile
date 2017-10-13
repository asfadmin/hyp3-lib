FROM ubuntu:16.04

ENV ISCE_VERSION=isce-20160906 \
    ISCE_HOME=/usr/local/isce \
    PATH=${PATH}:${ISCE_HOME}/bin:${ISCE_HOME}/applications \
    PYTHONPATH=${PYTHONPATH}:/usr/local

LABEL maintainer="Alaska Satellite Facility" \
    isce_version=${ISCE_VERSION}

# ISCE
ADD ./lib/${ISCE_VERSION}.tar.bz2 /usr/local
RUN mv /usr/local/${ISCE_VERSION} /usr/local/isce
