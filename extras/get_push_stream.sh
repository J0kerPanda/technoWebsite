# clone the project
git clone http://github.com/wandenberg/nginx-push-stream-module.git

# get desired NGINX version (works with 1.0.x, 0.9.x, 0.8.x series)
wget http://nginx.org/download/nginx-1.10.1.tar.gz && 
tar xzvf nginx-1.10.1.tar.gz && 
cd nginx-1.10.1 && 
./configure --add-module=../nginx-push-stream-module && 
make &&
sudo make install &&
sudo /usr/local/nginx/sbin/nginx -v