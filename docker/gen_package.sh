#!/bin/bash -x

cd /project

PKG_DIR=hack/docker/pkg

if [ -d $PKG_DIR ]; then
  rm -rf $PKG_DIR
fi
mkdir -p $PKG_DIR

#
# package an empty logs directory there
#
if [ -d $PKG_DIR/../../logs ]; then
  rm -rf $PKG_DIR/../../logs
fi
mkdir -p $PKG_DIR/../../logs

tar --exclude '.[giD]*' --exclude docker  -czvf $PKG_DIR/hack.tar.gz hack

cd /project/hack/docker
docker build --squash -t hack:v0.0.1 -f Dockerfile_invoice_hack .
#
# clean up
#
docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi

