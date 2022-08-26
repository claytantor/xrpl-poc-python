#!/bin/bash

if [[ ! -z "$1" ]]; then
    env="$1"
elif [[ "$CIRCLE_BRANCH" == "master" ]]; then
    env="prd"
elif [[ "$CIRCLE_BRANCH" == "dev" ]]; then
    env="dev"
else
    echo "Unable to determine environment"
    echo "usage: ./deploy.sh <env> or \$CIRCLE_BRANCH must be set"
    exit 1
fi

echo "using environment ${env}" 

if [[ $env == "dev" ]]; then
    dist_id=''
    s3_bucket='dev.xurl.org'
elif [[ $env == "prd" ]]; then
    dist_id='E3RWVWNCYFY2QA'
    s3_bucket='xurl.org'
fi

echo "using s3 bucket ${s3_bucket}"

# run this from site root
aws s3 sync $(pwd)/build/. s3://${s3_bucket} --acl public-read --delete --cache-control "public, max-age=31536000" --exclude "*.git/*" --exclude "*uploaded_images/*"

aws s3 cp s3://${s3_bucket}/index.html s3://${s3_bucket}/index.html --metadata-directive REPLACE --cache-control max-age=0 --content-type "text/html"

aws cloudfront create-invalidation --invalidation-batch "Paths={Quantity=1,Items=["/*"]},CallerReference=raypaygo-$(date +%s)" --distribution-id ${dist_id}