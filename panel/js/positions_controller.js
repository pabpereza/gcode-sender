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
				$('div.puesto'+index).addClass('active');
			}else
			{
				$('div.puesto'+index).removeClass('active');
			}
		}
		
	});

}


function change_active_position(position){

	$.post( url + 'positions' , { 'position': position }, function(){}, 'json');

	refresh_positions()
}


// MAIN
// First refresh of the positions
refresh_positions()

// Add event listener to the buttons
$('#boton').click(function(){
	console.log('click');
	position = $(this).attr('class').split(' ')[1];

	change_active_position(position);
	
});


