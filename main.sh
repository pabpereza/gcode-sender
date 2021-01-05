#!/bin/bash

while :; 
do 
	out=$(python3 reader.py)
	nPie=${out:3:-2}
	lastNumber=$nPie

	if [ "$nPie" != '' ] && [ "$nPie" != "$lastNumber" ]
	then
		./g_code_sender.py -p /dev/ttyACM0 -f GCodes/$nPie.gcode
	fi

done


	


