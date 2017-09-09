#!/bin/bash

#https://docs.travis-ci.com/user/deployment/script/#Ruby-version
rvm default exec fastlane --version

set -o allexport
rvm default exec fastlane --version
retcode=$?
set +o allexport

exit $retcode