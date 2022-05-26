// Script that call to and endpoint and panse a json response asynchronously
var url = 'http://localhost:8080/';


function refresh_positions() {

    $.getJSON(url + 'positions', {get_param: 'value'}, function (json) {

        for (positions in json) {
            position = json[positions];

            index = position['position']
            active = position['active']
            path = position['path']

            if (active) {
                let btn_puesto = $('#btn_puesto_' + index);
                btn_puesto.removeClass('btn-danger');
                btn_puesto.addClass('btn-success');
            } else {
                btn_puesto.removeClass('btn-success');
                btn_puesto.addClass('btn-danger');
            }
        }

    });

}


function change_active_position(position) {
    $.ajax(url + "positions", {
        data: JSON.stringify({'position': position}),
        method: "POST",
        contentType: "application/json",
        success: function (result) {
            refresh_positions();
        }
    });

}


// MAIN
// First refresh of the positions
refresh_positions();

// PROGRAMS
var gcode_programs = {};
$.ajax(url + "paths", {
    method: "GET",
    contentType: "application/json",
    success: function (result) {
        gcode_programs = result;
    }
});

// END PROGRAMS

// EVENTS
// Add event listener to the buttons
$('[id*="btn_puesto_"]').click(function () {
    change_active_position(this.id.split('_')[2]);
});

// Add event listener to the change program buttons
$('[id*="btn_program_"]').click(function () {
    let id_position = $(this).data("position");
    $('#modal_input_position').val(id_position);
    $('#modal_span_position').text(id_position);

    // Programs
    let modal_select_program = $('#modal_select_program');
    modal_select_program.empty();
    modal_select_program.append(new Option('Selecciona el programa', ''));

    for (let program of gcode_programs) {
        modal_select_program.append($('<option>', {
            value: program,
            text: program
        }));
    }
    $('#myModal').modal('show');
});

$('[id*="modal_btn_send"]').click(function () {
    // Update and refresh
    let position = $('#modal_input_position').val();
    let path = $('#modal_select_program').val();

    $.ajax(url + "position/path", {
        data: JSON.stringify({'position': position, 'path': path}),
        method: "UPDATE",
        contentType: "application/json",
        success: function (result) {
            console.log(result);
            refresh_positions();
        }
    });
});