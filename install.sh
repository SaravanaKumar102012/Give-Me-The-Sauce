#! /bin/bash

pkgs=( "requests" "bs4" "fake_useragent" "pysimplegui" )

for pkg in "${pkgs[@]}"
do
    python3 -m pip install $pkg
done
