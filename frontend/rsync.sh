#!/bin/bash
# 打包
echo "build..."
#npm run build
# 同步
echo "rsync..."
rsync -av ./dist/ root@8.218.190.223:/data2/chatgpt-web-share/frontend/dist
