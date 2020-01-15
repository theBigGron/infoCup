#!/bin/bash
echo "Starting Server"
python3 ./src/TorchSlave.py -ip http://192.168.178.50:8087 > /dev/null &
echo "Starting sim"
sleep 5
for i in {1..29};
do
  echo "Starting Run $i"
  ./ic20_linux -o /dev/null
done