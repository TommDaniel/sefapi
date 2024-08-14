#!/bin/bash

# Install Firefox
sudo apt-get update
sudo apt-get install -y firefox

# Install GeckoDriver
GECKODRIVER_VERSION=$(curl -sL https://github.com/mozilla/geckodriver/releases/latest | grep -oP '(?<=v)[\d\.]+')
wget https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz
tar -xvzf geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz
