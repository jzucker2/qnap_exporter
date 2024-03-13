# Configuration

## Example

### Quick with Environmental Variables

```
    ...
    environment:
      # this you can make up to be whatever you want, like `Living Room NAS`
      - QNAP_NAS_NAME=${QNAP_NAS_NAME}
      # like `10.0.1.1` or `qnap`
      - QNAP_NAS_HOST=${QNAP_NAS_HOST}
      # like `admin` or `jordan`
      - QNAP_NAS_USERNAME=${QNAP_NAS_USERNAME}
      # hopefully something secret!
      - QNAP_NAS_PASSWORD=${QNAP_NAS_PASSWORD}
```

### Multiple Routers with yaml config file

```yaml
nas_instances:
  - nas_name: Living Room NAS
    nas_host: 10.0.1.1
    nas_port: 8080
    nas_username: admin
    nas_password: foo

  - nas_name: Bedroom Room NAS
    nas_host: 10.0.1.2
    nas_port: 8080
    nas_username: admin
    nas_password: bar
```

## Development

I am using [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) to parse the YAML configs
