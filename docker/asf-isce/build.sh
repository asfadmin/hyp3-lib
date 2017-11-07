#! /bin/bash

# The following are expected in the context
# ./etc/${ISCE_VERSION}.tar.bz2

ISCE_VERSION=isce-20160906

aws s3 sync --exclude "*" --include "${ISCE_VERSION}.tar.bz2" s3://hyp3-docker/software/ ./etc/

docker build -t asf-isce:latest -f dockerfile .