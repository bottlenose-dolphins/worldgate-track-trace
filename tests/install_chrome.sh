#!/bin/bash

VERSION=109.0.5414.74-0ubuntu0.18.04.14
ARCH=amd64
URLBASE=https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+files

#download and install
wget ${URLBASE}/chromium-codecs-ffmpeg_${VERSION}_${ARCH}.deb \
&& wget ${URLBASE}/chromium-codecs-ffmpeg-extra_${VERSION}_${ARCH}.deb \
&& wget ${URLBASE}/chromium-browser_${VERSION}_${ARCH}.deb \
&& wget ${URLBASE}/chromium-chromedriver_${VERSION}_${ARCH}.deb \
&& apt-get update \
&& apt-get install -y ./chromium-codecs-ffmpeg_${VERSION}_${ARCH}.deb \
&& apt-get install -y ./chromium-codecs-ffmpeg-extra_${VERSION}_${ARCH}.deb \
&& apt-get install -y ./chromium-browser_${VERSION}_${ARCH}.deb \
&& apt-get install -y ./chromium-chromedriver_${VERSION}_${ARCH}.deb \
&& rm -rf /var/lib/apt/lists/*

# Download and Install chromedriver 
# wget -N https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip -P ~/
# unzip ~/chromedriver_linux64.zip -d ~/
# rm ~/chromedriver_linux64.zip
# sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
# sudo chown root:root /usr/local/bin/chromedriver
# sudo chmod 0755 /usr/local/bin/chromedriver


# # Install chrome broswer
# curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# apt-get -y update
# apt-get -y install google-chrome-stable