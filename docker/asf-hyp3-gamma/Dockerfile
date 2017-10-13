FROM asf-hyp3-base:latest

ENV GAMMA_VERSION=gamma_software_20161207

LABEL maintainer="Alaska Satellite Facility" \
    gamma_version=${GAMMA_VERSION}

# GAMMA
ADD ./lib/${GAMMA_VERSION}.tar.gz /usr/local
RUN mv /usr/local/${GAMMA_VERSION} /usr/local/gamma
