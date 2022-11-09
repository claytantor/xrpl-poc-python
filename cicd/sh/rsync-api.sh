#!/bin/bash

rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/. 