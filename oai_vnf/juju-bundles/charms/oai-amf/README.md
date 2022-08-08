# oai-amf

- mini params compare: 
PARAM                      COMPOSE            CHART             LOCAL
TZ                         Europe/Paris       -                 Europe/Paris 
SELECTED_0                 true               -                 true
SELECTED_1                 false              -                 false
NSSF_IPV4_ADDRESS          -                  127.0.0.1         oai-nssf
NSSF_FQDN                  -                  oai-nssf-svc      oai-nssf
NSSF_PORT                  -                  80                80
NSSF_API_VERSION           -                  v1                v1
MNC                        95                                   99
SERVED_GUAMI_MNC_0         95                                   99
PLMN_SUPPORT_MNC           95                                   99
PLMN_SUPPORT_TAC           0xa000                               0x0001
SD_0                       0xFFFFFF                             10203
SST_2                      222                                  2
SD_2                       123                                  2
SMF_IPV4_ADDR_0            192.168.70.133                       oai-smf
SMF_FQDN_1                 oai-smf                              localhost
SMF_IPV4_ADDR_1            0.0.0.0                              oai-smf
MYSQL_SERVER               192.168.70.131                       mysql
NRF_IPV4_ADDRESS           192.168.70.130                       oai-nrf
SMF_SELECTION              yes                no                  no
EXTERNAL_NSSF              no                 -                 -
AUSF_IPV4_ADDRESS          0.0.0.0                              oai-ausf
AUSF_FQDN                  localhost                            oai-ausf
UDM_IPV4_ADDRESS           0.0.0.0            -                 -
UDM_PORT                   80                 -                 -
UDM_API_VERSION            v2                 -                 -
UDM_FQDN                   localhost          -                 -
INT_ALGO_LIST              -                  ["NIA0","NIA1","NIA2"]     ["NIA0","NIA1","NIA2"]

## Description

TODO: Describe your charm in a few paragraphs of Markdown

## Usage

TODO: Provide high-level usage, such as required config or relations


## Relations

TODO: Provide any relations which are provided or required by your charm

## OCI Images

TODO: Include a link to the default image your charm uses

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.


## Notes
- pod port for main container is not proper and it should to be changed.
- selected-0 not exists in deployment config but was in compose