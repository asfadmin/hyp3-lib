#! /bin/bash

# The following is expected in the context:
# ./etc/${MAPREADY_VERSION}.tar.gz

MAPREADY_VERSION=ASF_MapReady

aws s3 sync --exclude "*" --include "${MAPREADY_VERSION}.tar.gz" s3://hyp3-docker/software/ ./etc/

docker build -t asf-base:latest -f dockerfile .
