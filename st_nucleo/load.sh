#!/bin/sh

lastsauvegarde=$(ls -rt ~/Downloads | tail -n 1)
scp  /home/lasagne/Downloads/$lastsauvegarde pi@192.168.1.13:maison/st_nucleo/prog.NUCLEO_F446RE.bin
ssh pi@192.168.1.13 "sudo cp maison/st_nucleo/prog.NUCLEO_F446RE.bin maison/st_nucleo/carte/prog.NUCLEO_F446RE.bin"
sleep 60
echo "ok c'est bon"
