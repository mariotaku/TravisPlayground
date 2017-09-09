#!/bin/bash

echo $PATH

fastlane --version

set -o allexport
fastlane --version
retcode=$?
set +o allexport

exit $retcode