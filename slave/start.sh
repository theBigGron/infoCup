#!/bin/bash
echo "Starting Server"
python3 ./python/TorchMain.py -p 5000 -ip http://192.168.178.50:8087 > /dev/null &
sleep 5
echo "Starting sim"
for i in {1..31};
do
  echo "Starting Run $i"
  ./ic20_linux -u http://localhost:5000
done