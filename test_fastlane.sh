#!/bin/bash

#https://docs.travis-ci.com/user/deployment/script/#Ruby-version
rvm use default

echo $PATH

fastlane --version

set -o allexport
fastlane --version
retcode=$?
set +o allexport

exit $retcode