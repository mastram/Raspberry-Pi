$(document).ready(function (){

	$("#shutdown-now").click(function(){
		
		$.post("rpi_util.php",
			{code:"shutdown-now"},
			function(data,status){$("#debug-info").text(data);}
		);
	
	});

	$("#reboot-now").click(function(){
		
		$.post("rpi_util.php",
			{code:"reboot-now"},
			function(data,status){$("#debug-info").text(data);}
		);
	
	});

});