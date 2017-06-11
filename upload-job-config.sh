#!/bin/sh -e

~/src/jenkins-tools/bin/delete-job.sh mail-bug || true
~/src/jenkins-tools/bin/put-job.sh mail-bug job.xml
