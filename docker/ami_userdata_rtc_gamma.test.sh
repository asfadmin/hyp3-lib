#!/bin/bash
set -x

aws s3 cp s3://hyp3-config/awslogs.test.conf /tmp/awslogs.conf
curl https://s3.amazonaws.com//aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O
python awslogs-agent-setup.py --region us-east-1 --non-interactive --configfile /tmp/awslogs.conf

# Assumes that AWS Linux AMI is being used.
sudo yum update -y
sudo yum install docker -y

# If Ubuntu is the host AWS AMI
# sudo apt-get update
# sudo apt-get install docker -y

sudo service docker start

sudo $(aws ecr get-login --region us-east-1)

# {1} is the docker image (including repo, name and tag), and {0} is the proc program
sudo docker run --rm {1} python {0} --verbose -n 10

sleep 60
poweroff
