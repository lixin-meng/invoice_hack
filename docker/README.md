## local test

To test with docker
```
cd docker

#
# generate the code package
#
#
# update version info first !!!

gen_package.sh

```
```
#
# build the Smart Invoice Hack image on top of cfd_python_3.6 image
#

docker build --squash -t invoice_hack:v0.0.1 -f Dockerfile_invoice_hack .
```

```
docker push invoice_hack:v0.0.1
```

## docker run locally

```
docker-compose up hack
```
