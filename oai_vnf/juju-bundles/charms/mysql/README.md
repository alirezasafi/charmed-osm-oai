# mysql
### Mini Deployment
- use mini database initialization. and data persistence is off.


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
- volume sql database:
    the sql databse should be mounted to the proper path.

- liveness and readiness prbe:
    - use mysql-healthcheck.sh script for both of probes.
    - failed with command: "sh -c mysqladmin ping -u root -p${MYSQL_ROOT_PASSWORD}". 
        error log: Enter password: mysqladmin: connect to server at 'localhost' failed
error: 'Access denied for user 'root'@'localhost' (using password: NO)' Enter password: mysqladmin: Unknown command: 'linux'.
