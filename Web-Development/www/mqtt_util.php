<?php

$code = $_POST["code"];

if($code == "start-tracking"){
	
	$response_code = send_command_to_device("Start");
	if($response_code == 200 || $response_code == 202){
		echo "Start Command sent to device";
	}
	else{
		echo "Could not send start command to device. Status Code: " . $response_code;
	}
}

if($code == "stop-tracking"){
	
	$response_code = send_command_to_device("Stop");
	if($response_code == 200 || $response_code == 202){
		echo "Stop Command sent to device";
	}
	else{
		echo "Could not send stop command to device. Status Code: " . $response_code;
	}
	
}

function send_command_to_device($command){

	$url = 'https://1e4bcf9a-3f25-45c3-85e2-f3a486ad18f6.canary.cp.iot.sap/iot/core/api/v1/devices/10/commands';

	$fields = array(
		'capabilityId'  => 'ea5cfc21-6e3a-4957-a314-926d1de20fd1',
		'sensorId'	=> '17',
		'command'      	=> array( 'command' => $command )
	);

	$headers = array(
		'Authorization: Basic ' . base64_encode("root:n0zfl5DDgimJ63O"),
		'Content-Type: application/json'
	);

	// Open connection
	$ch = curl_init();
		
	// Set the url, number of POST vars, POST data
	curl_setopt( $ch, CURLOPT_URL, $url );

	curl_setopt( $ch, CURLOPT_POST, true );
	curl_setopt( $ch, CURLOPT_HTTPHEADER, $headers);
	curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );

	curl_setopt( $ch, CURLOPT_POSTFIELDS, json_encode( $fields ) );
	
	// Execute post
	$result = curl_exec($ch);
	$response = curl_getinfo( $ch );

	// Close connection
	curl_close($ch);

	$code = $response['http_code'];
	return $code;

	//return 200;
}

?>
