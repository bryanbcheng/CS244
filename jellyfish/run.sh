#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

bwnet=100 #Mbs
delay=5

iperf_port=5001

#python jellyfish.py -nse 16 -nsw 20 -np 4
python jellyfish.py -nse 2 -nsw 3 -np 3