#!/bin/sh -e

# shellcheck disable=SC2016
jjm --locator https://github.com/FunTimeCoding/mail-bug.git --build-command script/build.sh --junit build/junit.xml --checkstyle 'build/log/checkstyle-*' --recipients funtimecoding@gmail.com > job.xml
