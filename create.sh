#!/usr/bin/env bash

JSON_NAME=${1}
CONFIG=${2}

generate-dashboard -o ${JSON_NAME} ${CONFIG}

payload="{\"dashboard\": $(jq . frontend.json), \"overwrite\": false}"

curl -X POST -H "Authorization: Bearer eyJrIjoiNUdxNE5jczlETFdvOW5aNVhJU05KS2YzOUVMMGVjQTUiLCJuIjoiYWRtaW4iLCJpZCI6MX0=" \
  -H "Content-Type: application/json" \
  -d "${payload}" \
  "http://admin:admin@localhost:3000/api/dashboards/db"
