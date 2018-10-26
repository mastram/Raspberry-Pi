#Startup Scripts

##Print IP
Print IP if the Sense hat is connected
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi


## Start MQTT
sudo sh /home/pi/Desktop/startup_scripts/start_mqtt.sh

exit 0
