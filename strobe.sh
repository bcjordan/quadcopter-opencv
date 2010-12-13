#!/bin/sh
#
# Blink the onboard LED

GPIO=$1

cleanup() { # Release the GPIO port
  echo $GPIO > /sys/class/gpio/unexport
  exit
}

# Open the GPIO port
#
echo $GPIO > /sys/class/gpio/export 

trap cleanup SIGINT # call cleanup on Ctrl-C

# Blink forever
while [ "1" = "1" ]; do
  echo "high" > /sys/class/gpio/gpio$GPIO/direction 
  sleep 1
  echo "low" > /sys/class/gpio/gpio$GPIO/direction  
  sleep 1
done

cleanup # call the cleanup routine
