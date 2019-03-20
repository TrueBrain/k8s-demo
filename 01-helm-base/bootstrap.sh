#!/bin/sh

set -e

# External CRDs; helm doesn't support CRDs that well, so we apply it manually
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/master/deploy/manifests/00-crds.yaml

helm dep update charts/test-base
helm upgrade \
    --force \
    --set cert-manager.createCustomResource=false \
    --install test-base \
    charts/test-base
