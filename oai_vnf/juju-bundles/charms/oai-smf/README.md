# oai-smf
# NOTES
default-dns-ipv4-address: configure dns for ue. don't use k8s dns. it can be 8.8.8.8 or 4.4.4.4 if you don't know your dns.
default-dns-sec-ipv4-address: configure dns for ue. don't use k8s dns. it can be 8.8.8.8 or 4.4.4.4 if you don't know your dns
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
- protocol could unset in container ports!