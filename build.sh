#!/usr/bin/bash
export APP_VERSION=0.`git log --oneline | wc -l`

if [ "$1" == "log" ]
then
  buildozer android debug deploy run logcat
else
  buildozer android debug deploy run
fi
