#!/bin/sh
# unpacks all dependencies

tar zxvf django.tar.gz
mv django hitsearch/
tar zxvf httplib2.tar.gz
mv httplib2 hitsearch/crawler/
