#! /bin/bash

# The following are expected in the context
# ./etc/${GAMMA_VERSION}.tar.gz

GAMMA_VERSION=gamma_software_20161207

aws s3 sync --exclude "*" --include "${GAMMA_VERSION}.tar.gz" s3://hyp3-docker/software/ ./etc/

docker build -t asf-gamma:latest -f dockerfile .