$(document).ready(function (){

	$("#start-tracking").click(function(){
		
		$.post("mqtt_util.php",
			{code:"start-tracking"},
			function(data,status){$("#debug-info").text(data);}
		);
	
	});

	$("#stop-tracking").click(function(){
		
		$.post("mqtt_util.php",
			{code:"stop-tracking"},
			function(data,status){$("#debug-info").text(data);}
		);
	
	});

});