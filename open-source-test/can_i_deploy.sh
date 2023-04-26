#!/bin/bash
CLIENT_VERSION=$1
if [ -x $CLIENT_VERSION ]; then
    echo "ERROR: You must specify a Client version"
    exit
fi
PROVIDER_VERSION=$2
if [ -x $PROVIDER_VERSION ]; then
    echo "ERROR: You must specify a Provider version"
    exit
fi

pact-broker can-i-deploy --pacticipant RadioBrowserClient\
                         --version $CLIENT_VERSION\
                         --broker-base-url=http://localhost:9292\
                         --pacticipant RadioBrowser\
                         --version $PROVIDER_VERSION\



