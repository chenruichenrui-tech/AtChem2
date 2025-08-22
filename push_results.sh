#!/bin/bash
# push_results.sh —— 把最新结果同步到 GitHub
set -e

# 1. 复制
cp -r model/output/* OUT/

# 2. 如果 reactionRates 目录里有大量数字文件，只保留一个摘要
find OUT/reactionRates -type f -name '*[0-9]' | head -n 100 > /tmp/rr.list || true
if [ -s /tmp/rr.list ]; then
    echo "$(wc -l < /tmp/rr.list) reaction-rate files; keeping first 10 as sample"
    mkdir -p OUT/reactionRates_sample
    head -n 10 /tmp/rr.list | xargs -I{} cp {} OUT/reactionRates_sample/
    rm -rf OUT/reactionRates
    mv OUT/reactionRates_sample OUT/reactionRates
fi

# 3. 提交
git add OUT/
git commit -m "Update results $(date +%Y%m%d_%H%M%S)"
git push origin master