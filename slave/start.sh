#!/bin/bash
echo "Starting Server"
#http://accum.informatik.uni-oldenburg.de:11001
python3 ./src/TorchSlave.py -p 5000 -ip http://localhost:8087 > /dev/null &
sleep 5
echo "Starting sim"
for i in {1..31};
do
  echo "Starting Run $i"
  ./ic20_linux -u http://localhost:5000
done