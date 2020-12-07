#!/bin/bash
cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
cd /usr/local/ev_sdk/authorization
chmod +x ev_license
./ev_license -r r.txt
./ev_license -l privateKey.pem r.txt license.txt
cp /usr/local/ev_sdk/authorization/license.txt /usr/local/vas/license.txt
a=`cat license.txt|sed 's/{"license":"\(.*\)","version":7}/\1/g'`
cd /usr/local/vas
sed -i "s/license=/license=$a/g" local.conf
sed -i 's/version=/version=7/g' local.conf

wait
source /etc/profile
bash /usr/local/vas/vas_stop.sh
bash /usr/local/vas/vas_start.sh