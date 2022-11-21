#!/bin/bash

rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python/api ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/xrpl-poc-python/. 
rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python/migrations ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/xrpl-poc-python/. 
rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python/env ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/xrpl-poc-python/. 
rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python/devops ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/xrpl-poc-python/. 
rsync -Pav -e "ssh -i $HOME/data/keys/claytantor-oregon.pem" $HOME/data/github.com/claytantor/xrpl-poc-python/requirements.txt ubuntu@ec2-34-211-56-213.us-west-2.compute.amazonaws.com:/home/ubuntu/xrpl-poc-python/. 
