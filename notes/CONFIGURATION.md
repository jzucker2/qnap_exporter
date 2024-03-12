# Configuration

## Example

### Quick with Environmental Variables

```
    ...
    environment:
      # like `http://10.0.1.1`
      - QNAP_HOST_IP=${QNAP_HOST_IP}
      # this you can make up to be whatever you want, like `Living Room NAS`
      - QNAP_HOST_NAME=${QNAP_HOST_NAME}
      - QNAP_USERNAME=${QNAP_USERNAME}
      # hopefully something secret!
      - QNAP_PASSWORD=${QNAP_PASSWORD}
```

### Multiple Routers with yaml config file

```yaml
qnap_instances:
  - qnap_name: Living Room NAS
    qnap_ip: http://10.0.1.1
    qnap_username: admin
    qnap_password: foo

  - qnap_name: Bedroom Room NAS
    qnap_ip: http://10.0.1.2
    qnap_username: admin
    qnap_password: bar
```

## Development

I am using [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) to parse the YAML configs
