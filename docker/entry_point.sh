#!/bin/bash

set -e
. ~/.bashrc

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

# Add python as command if needed
if [ "${1:0:1}" = '-' ]; then
	set -- python "$@"
fi

test -d /tmp/rdisk || mkdir -p /tmp/rdisk

# Drop root privileges if we are running python
# allow the container to be started with `--user`
#
if [ "$(id -u)" = '0' ] && [ "$1" = 'gunicorn' -o "$1" = 'python' ]
then
    #
    # Change the ownership of user-mutable directories to hack
    #
    for path in \
        /tmp/rdisk \
    ; do
        test -d "$path" && chown -R cfd:cfd "$path"
    done

    #
    # when running with kubectl, it doesn't like the quote around the command,
    # especially when there's arguments
    #
    set -- gosu cfd $@
fi

# As argument is not related to python,
# then assume that user wants to run his own process,
# for example a `bash` shell to explore this image
exec $@


# test with docker
#  docker build -t chat_flow:0.5 -f Dockerfile_chat_flow .
#  docker-compose up ml
# or
#  docker rm ml && \
#    docker run -it -p "5000:5000" -e "PYTHONPATH=/project/chat_flow" \
#     -v /Users/lixin.meng/project:/project \
#     -v /Users/lixin.meng/tmp:/tmp/rdisk \
#     --name ml ml /bin/bash -c 'python /project/chat_flow/api/app.py'

# test with kubectl
#
#  minikube start
#  eval $(minikube docker-env)
#  docker build -t chat_flow:0.5 -f Dockerfile_chat_flow .
#
#  kubectl run ml-pod  --image=chat_flow:0.5 --port=5000
#  kubectl expose deployment  ml-pod --type=LoadBalancer
#  kubectl get pods
#  kubectl port-forward ml-pod-.....-... 5000
#  kubectl delete service
#  kubectl delete service ml-pod
#  kubectl delete deployment ml-pod
#  eval $(minikube docker-env -u)
#  minikube stop
