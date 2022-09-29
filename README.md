# Open Air Interface 5G CORE and RAN Deployment using OSM
OAI 5G core network have different network functions which can be used invidiually or deployed all together in different combination on a production grade Kubernetes cluster.

**Core Services:**
1.   Mysql
2.   NRF
3.   SMF
4.   UPF(SPGWU)
5.   AMF

**RAN Services:**
1.   gNBRFsim
2.   NR-UE

Each network function is deployed in a pod and these pods are distrubuted
among different nodes.

## Pre-requisite
The cluster on which these Charms will be deployed should have RBAC and [Multus CNI](https://github.com/k8snetworkplumbingwg/multus-cni). Multus is necessary to provide multiple interfaces to AMF and UPF/SPGWU
## Deployment.

> To create osm vnf and ns package, use the following commands which will
> generate a vnf package structure named oai-vnf and ns package structure
> named oai-ns

```bash
# in the rep root dir execute the following commands.
osm nfpkg-create oai_vnf/
osm nspkg-create oai_ns/
```

> Onboarded package can be verified with the following commands.

```bash
osm nfpkg-list # or use osm vnfd-list
osm nspkg-list # or use osm nsd-list
```

### Create dummy VIM account

> Create a dummy vim that can be used when the k8scluster being added to osm.

```bash
osm vim-create --namd <vim-name> --account_type dummy
```
> if there is a proper VIM like openstack, use the following command.

```bash
osm vim-create --name <vim-name> --user <username> --password <password> \
    --auth_url <openstack-url> --tenet <tenant-name> --account_type openstack
```
* `vim-name` is the name of the vim being created.
* `username` and `password` are the credentials of openstack.
* `tenant-name` is the tenant to be assosiated to the user in the openstack.
* `openstack-url` is the url of openstack which will be used as VIM.

### Add k8s-cluster
> K8scluster used to attach a cluster with OSM which will be used for knf deployment.


```bash
osm k8scluster-add --creds <k8s-config-file>  --version v1 --vim <vim-name> --description 'K8s Cluster for KNFs' --k8s-nets '{"net1": "vim-net"}' <cluster-name>
```

* `k8s-config-file` is the configuration file of kubernetes cluster.

### Instantiating of the oa network service.

> To instantiating the oai network service use the following command.
```bash
osm ns-create --ns_name <ns-name> --nsd_name oai-ns --vim_account <vim-name>
```

> To verifying the instantiating process use the following commands.

```bash
# with the osm client
osm ns-list
# for detail information
osm ns-show
# use kubectl command.
kubectl -n oai-kdu-*** get pods
```

## Notes
### Charm Notes
- `metadata.yaml` file must has `summary` field 
- every hook file should start with executable line related to the file. e.g py file: `#!/usr/bin/env python3`
 

### Container IP that created by multus plugin:
    - AMF: 172.21.6.201
    - SPGWU: 172.21.6.200
    - NR-UR: 172.21.6.204
    - GNB: 172.21.6.202 , 172.21.6.203