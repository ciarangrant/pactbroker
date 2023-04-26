#!/bin/bash
VERSION=$1
if [ -x $VERSION ]; then
    echo "ERROR: You must specify a provider version"
    exit
fi

#THIS WORKS FOR 1 TEST
pipenv run pact-verifier --provider-base-url=https://nl1.api.radio-browser.info/\
  --pact-url="https://thegrant.pactflow.io/pacts/provider/RadioBrowser/consumer/RadioBrowserClient/latest" \
  --provider-app-version $VERSION \
  --provider-version-branch main \
  --pact-broker-token g0wWA7F8Ip5SYI3l2z4HEA \
  --publish-verification-results
