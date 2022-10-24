#!/bin/bash

helm install --namespace oai cassandra cassandra/
helm install --namespace oai oai-hss oai-hss/
helm install --namespace oai redis redis/
helm install --namespace oai magma-mme magma-mme/
helm install --namespace oai oai-spgwc oai-spgwc/
helm install --namespace oai oai-spgwu oai-spgwu/
helm install --namespace oai trf-gen trf-gen/
helm install --namespace oai flexran flexran/
helm install --namespace oai enb enb/
helm install --namespace oai oai-ue oai-ue/
