#!/bin/bash

if [ "$1" != "" ]; then
    exec "$@"
    exit
fi

chmod +x compose/start.sh
./compose/start.sh