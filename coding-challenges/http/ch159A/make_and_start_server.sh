# sudo apt-get install build-essential cmake

echo building the Rainbow Server...
mkdir -p rainbowserver-build
cd rainbowserver-build
cmake ../rainbowserver > /dev/null
make > /dev/null
echo build the Rainbow Server complete

echo Now create the raibow and start the serve, it will take 1~3 minute.
echo when you see 'Server is running...', you can type 'python ../ch159.py' in another terminal.

./rainbowserver rainbow.data 127.0.0.1 9527





