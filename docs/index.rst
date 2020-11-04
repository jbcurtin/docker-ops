##########
docker-ops
##########

`docker-ops` was created to automate versioning and rapid deployment of Docker Images into the Cloud

Getting Started
---------------

Lets assume the directory `images` exists in the root level of a repository. Folder names created in the `images` directory specific the names of docker images. For example:

`images/redis` would be tagged as `redis:0.0.1` and `redis:latest`

To generate the redis image, contents of `images/redis` need to follow one of two directory structures. Either have a `Dockerfile` or `Dockerfiles` folder in the directory

We’ll start with an example of the Dockerfile:

The folder structure of the Dockerfile inside `images/redis` looks like

With the example created, build and deploy the image to DockerHub with the script

.. code-block:: bash

    #!/usr/bin/env bash  
    
    set -e  
    if [ ! -d "env" ]; then     
        virtualenv -p $(which python) venv
        fi 
        # Docker Hub export IMAGE_REGISTRY_DOMAIN='<dockerhub-login>' source venv/bin/activate
        pip install -U pip
        pip install -U docker-ops
        docker login docker-ops.py -s -d $PWD/images  
    fi

Go ahead and build the image.

Interested in helping improve `docker-ops`? Open an issue request here: https://github.com/jbcurtin/docker-ops/issues!

.. toctree::
    :maxdepth: 2

