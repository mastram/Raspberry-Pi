<?php
require_once( 'config.php' );

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

	global $iot_service_url, $iot_service_user, $iot_service_password;
	global $iot_service_cap_id, $iot_service_sensor_id;
	$url = $iot_service_url;
	$auth_string = $iot_service_user.":".$iot_service_password;

	$fields = array(
		'capabilityId'  => $iot_service_cap_id,
		'sensorId'	=> $iot_service_sensor_id,
		'command'      	=> array( 'command' => $command )
	);

	$headers = array(
		'Authorization: Basic ' . base64_encode($auth_string),
		'Content-Type: application/json'
	);

	//echo "111"; var_dump($url);
	//echo "222"; var_dump($fields);
	//echo "333"; var_dump($headers);

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
