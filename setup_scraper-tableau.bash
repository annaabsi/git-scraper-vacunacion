#!/bin/bash
echo 'STARTED setup_scraper-tableau'
echo 'WGET downloading'
wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.128-1_amd64.deb -O google.deb
echo 'INSTALL deb package'
sudo dpkg -i google.deb
echo 'INSTALL apt dependencies listed on Aptfile'
sudo apt-get install $(grep -vE "^\s*#" Aptfile  | tr "\n" " ")
echo 'FINISHED setup_scraper-tableau'