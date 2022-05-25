// Script that call to and endpoint and panse a json response asynchronously
var url = 'http://localhost:8080/';


function refresh_positions(){

	$.getJSON( url + 'positions', { get_param: 'value' }, function(json) {
		
		for( positions in json){
			position = json[positions];
			
			index = position['position']
			active = position['active']
			path = position['path']
			
			if(active == true){
				$('#btn_puesto_'+index).removeClass('btn-danger');
				$('#btn_puesto_'+index).addClass('btn-success');
			}else
			{
				$('#btn_puesto_'+index).removeClass('btn-success');
				$('#btn_puesto_'+index).addClass('btn-danger');
			}
		}
		
	});

}


function change_active_position(position){
	$.ajax(url + "positions", {
		data: JSON.stringify({'position': position }),
		method: "POST",
		contentType: "application/json",
		success: function(result) {
			refresh_positions();
		}
	});

}


// MAIN
// First refresh of the positions
refresh_positions()

// Add event listener to the buttons
$('[id*="btn_puesto_"').click(function(){
	change_active_position(this.id.split('_')[2]);
});

// Add event listener to the change program buttons
$('[id*="btn_program_"').click(function(){
	let id_position = $( this ).data("position");
	$('#modal_input_position').val(id_position);
	$('#modal_span_position').text(id_position);
	$('#myModal').modal('show');
});
