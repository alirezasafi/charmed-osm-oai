#!/bin/bash


helm uninstall --namespace oai cassandra
helm uninstall --namespace oai oai-hss
helm uninstall --namespace oai redis 
helm uninstall --namespace oai magma-mme 
helm uninstall --namespace oai oai-spgwc 
helm uninstall --namespace oai oai-spgwu 
helm uninstall --namespace oai trf-gen 
helm uninstall --namespace oai flexran
helm uninstall --namespace oai enb 
helm uninstall --namespace oai oai-ue 
