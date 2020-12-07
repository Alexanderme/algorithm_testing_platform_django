#/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
cd /usr/local/ev_sdk/authorization
chmod +x ev_license
./ev_license -r r.txt
./ev_license -l privateKey.pem r.txt license.txt
cp /usr/local/ev_sdk/authorization/license.txt  /usr/local/ev_sdk/bin
cp /usr/local/ev_sdk/authorization/license.txt /usr/local/ias/license_conf.json
bash /usr/local/ias/ias_stop.sh
bash /usr/local/ias/ias_start.sh  &


