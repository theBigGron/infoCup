#!/bin/bash
echo "Starting Server"
python3 ./src/TorchSlave.py -ip http://accum.informatik.uni-oldenburg.de:11001 > /dev/null &
echo "Starting sim"
sleep 5
for i in {1..30};
do
  echo "Starting Run $i"
  ./ic20_linux -o /dev/null
done