#!/bin/bash

#https://docs.travis-ci.com/user/deployment/script/#Ruby-version
rvm $TRAVIS_RUBY_VERSION

echo $PATH

fastlane --version

set -o allexport
fastlane --version
retcode=$?
set +o allexport

exit $retcode