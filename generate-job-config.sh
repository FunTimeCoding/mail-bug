#!/bin/sh -e

# shellcheck disable=SC2016
jjm --locator https://github.com/FunTimeCoding/mail-bug.git --build-command ./build.sh --junit build/junit.xml > job.xml
