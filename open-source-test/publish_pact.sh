export PACT_BROKER_BASE_URL="http://localhost:9292"
#pact-broker publish /Users/cgrant/GDS/Pact/docker/python/open-source-test/tests/radiobrowserclient-radiobrowser.json --consumer-app-version 1.0.0 --branch main --broker-base-url http://localhost:9292
export PACT_BROKER_USERNAME="ciaran@thegrant.org.uk"
export PACT_BROKER_PASSWORD="8qeRLqXQqE"
export PACT_BROKET_TOKEN="g0wWA7F8Ip5SYI3l2z4HEA"
#bundle exec bin/pact-broker publish $(dirname "$0")/pact.json --consumer-app-version=1.0.0 --tag master --verbose
#bundle exec /usr/local/bin/pact-broker publish /Users/cgrant/GDS/Pact/python/open-api/tests/radiobrowserclient-radiobrowser.json --consumer-app-version=0404231548 --tag main --verbose
