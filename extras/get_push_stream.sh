# clone the project
git clone https://github.com/wandenberg/nginx-push-stream-module.git
NGINX_PUSH_STREAM_MODULE_PATH=$PWD/nginx-push-stream-module

# get desired nginx version (works with 1.2.0+)
wget http://nginx.org/download/nginx-1.10.0.tar.gz

# unpack, configure and build
tar xzvf nginx-1.10.0.tar.gz
cd nginx-1.10.0
./configure --add-module=../nginx-push-stream-module
make

# install and finish
sudo make install

# check
sudo /usr/local/nginx/sbin/nginx -v
    nginx version: nginx/1.2.0

# test configuration
sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf -t

# run
#sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf