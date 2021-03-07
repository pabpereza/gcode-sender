#!/bin/bash

lastNumber=""

while :; 
do 
	echo "Buscando QR"
	out=$(python3 reader.py)
	out2=$( echo $out | tr -d \' )
	nPie=$( echo $out2 | tr -d \b )

	echo "Numero de pie: "$nPie
	echo "Úlitmo número: "$lastNumber

	if [ "$nPie" != '' ] && [ "$nPie" != "$lastNumber" ]
	then
		./g_code_sender.py -p /dev/ttyACM0 -f GCodes/$nPie.gcode
	fi
	
	lastNumber=$nPie
done


	


