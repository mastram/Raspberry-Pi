cd /home/pi;
sleep 3
su pi -c 'python /home/pi/Pi-Projects/mqtt-client.py >> /home/pi/mqtt.log 2>&1 &'
