#!/bin/bash

osm nfpkg-create oai_vnf
osm nspkg-create oai_ns
osm ns-create --ns_name oai-ns --nsd_name oai-ns --vim_account hackfest-dummy --config_file params.yaml