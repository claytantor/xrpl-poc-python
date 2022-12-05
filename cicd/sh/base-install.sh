#!/bin/bash

sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade

sudo apt update
sudo apt install docker.io
curl https://pyenv.run | bash

sudo apt-get -y install build-essential libssl-dev libffi-dev python3-dev checkinstall
sudo apt-get -y install libncursesw5-dev libgdbm-dev libc6-dev
sudo apt-get -y install zlib1g-dev libsqlite3-dev tk-dev
sudo apt-get -y install libssl-dev openssl
sudo apt-get -y install libffi-dev
sudo apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
sudo groupadd docker
sudo usermod -aG docker $USER

# vi ~/.bashrc
# source ~/.bashrc
# pyenv install 3.9.1
# pyenv virtualenv 3.9.1 xurlpay
# docker ps
# sudo groupadd docker
# sudo usermod -aG docker $USER
# docker run hello-world



