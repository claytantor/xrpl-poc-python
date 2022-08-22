docker run -dit \
    --name rippled \
    -p 8082:80 \
    -p 5005:5005 \
    -v $(pwd)/config/:/config/ \
    xrpllabsofficial/xrpld:latest