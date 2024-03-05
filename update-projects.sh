#!/usr/bin/env bash

HERE="$(cd $(dirname $0);pwd)"
echo "[INFO][WORKDIR] ${HERE}"
cd "${HERE}"

echo "[INFO] auto-update"
git pull

echo "[INFO][RUN] ${HERE}/main.sh"
"${HERE}/main.sh" "${@}"
