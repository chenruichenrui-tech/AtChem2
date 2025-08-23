#!/bin/bash
set -e
cp -r model/output/* OUT/
git add OUT/
git commit -m "Update results $(date +%Y%m%d_%H%M%S)"
git push origin master
