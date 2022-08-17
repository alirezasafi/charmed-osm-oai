#!/bin/bash

VIM_NAME="hackfest-dummy"
K8S_CONFIG_PATH="/etc/kubernetes/admin.conf"
osm vim-create --name $VIM_NAME --account_type dummy
osm k8scluster-add --creds $K8S_CONFIG_PATH --version v1 --vim $VIM_NAME --description "My K8s cluster" --k8s-nets '{"net1": "vim-net"}' cluster