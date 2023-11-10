# Curl Commands

```
curl -i "http://10.0.1.104:2003/api/v1/qnap/debug" \
-H "Content-Type: application/json"
```

## Dev

```
curl -i "http://localhost:2003/api/v1/qnap/debug" \
-H "Content-Type: application/json"

curl -i "http://localhost:2003/api/v1/qnap/debug/pprint" \
-H "Content-Type: application/json"

curl -i "http://localhost:2003/api/v1/qnap/exporter/simple" \
-H "Content-Type: application/json"

curl -i "http://localhost:2003/api/v1/qnap/exporter/metrics/update" \
-H "Content-Type: application/json"
```
