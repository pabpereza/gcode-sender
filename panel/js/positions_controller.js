// Script that call to and endpoint and panse a json response asynchronously
var url = 'http://localhost:8080/';
var path_modal_explorer = '/gcodes';


function refresh_positions() {

    $.getJSON(url + 'positions', {get_param: 'value'}, function (json) {

        for (positions in json) {
            position = json[positions];

            index = position['position']
            active = position['active']
            path = position['path']
            let btn_puesto = $('#btn_puesto_' + index);
            let puesto_program = $('#puesto_program_' + index);

            if (path.length > 2) {
                puesto_program.text(path);
            } else {
                puesto_program.text("Programa no cargado");
            }
            if (active) {
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


function show_alert_danger() {
    $('#alert_danger').addClass('show');
    setTimeout(() => {
        $('#alert_danger').removeClass('show');
    }, 2000);
}

function show_alert_success() {
    $('#alert_success').addClass('show');
    setTimeout(() => {
        $('#alert_success').removeClass('show');
    }, 2000);
}

function generate_file_manager(paths) {
    $("#files").simpleFileBrowser({
        json: paths,
        path: path_modal_explorer,
        view: 'icon',
        select: false,
        breadcrumbs: true,
        onOpen: function (obj, file, folder, type) {
            if (type == 'file') {
                alert("Open file: " + folder + '/' + file);
            }
            path_modal_explorer = folder;
        }
    });
}


// MAIN
// First refresh of the positions
refresh_positions();

// PROGRAMS
var gcode_programs = {
    '/': [
        {
            name: 'gcodes',
            type: 'folder'
        }
    ]
};
$.ajax(url + "paths", {
    method: "GET",
    contentType: "application/json",
    success: function (result) {
        //gcode_programs = result;
        result.forEach((path) => {
            let parts = path.split('/');

            // Add files
            let file = parts.pop();
            let path_without_file = "/" + parts.join("/");

            if (!(path_without_file in gcode_programs)) {
                gcode_programs[path_without_file] = [];
            }
            gcode_programs[path_without_file].push({
                name: file,
                type: 'gcode'
            });

            // Add dirs
            let dir = parts.pop();
            let path_without_file_and_dir = "/" + parts.join("/");

            if (!(path_without_file_and_dir in gcode_programs)) {
                gcode_programs[path_without_file_and_dir] = [];
            }

            let has_dir = false;
            gcode_programs[path_without_file_and_dir].forEach((x) => {
                if (x.name === dir) {
                    has_dir = true;
                }
            });

            if (!has_dir) {
                gcode_programs[path_without_file_and_dir].push({
                    name: dir,
                    type: 'folder'
                });
            }
        });
    }
});


let paths = {

    '/': [
        {
            name: 'AC-DC - The Very Best',
            type: 'folder'
        },
        {
            name: 'Metallica - Best of the best',
            type: 'folder'
        },
        {
            name: 'index.html',
            type: 'html'
        }
    ],

    '/AC-DC - The Very Best': [
        {
            name: '..',
            type: 'folder'
        },
        {
            name: '01 Hard As A Rock.mp3',
            type: 'mp3'
        },
    ],

    '/Metallica - Best of the best': [
        {
            name: '..',
            type: 'folder'
        },
        {
            name: 'Disc One',
            type: 'folder'
        },
    ]
}
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
    //$('#modal_span_position').text(id_position);

    //
    $('#modal_body_data').html('<div id="files"></div>');
    generate_file_manager(gcode_programs);
    // Programs
    /*let modal_select_program = $('#modal_select_program');
    modal_select_program.empty();
    modal_select_program.append(new Option('Selecciona el programa', ''));

    for (let program of gcode_programs) {
        modal_select_program.append($('<option>', {
            value: program,
            text: program
        }));
    }*/
    $('#myModal').modal('show');
});

$('[id*="modal_btn_send"]').click(function () {
    // Update and refresh
    let position = $('#modal_input_position').val();
    let path = $('#modal_select_program').val();

    $.ajax(url + "position/path", {
        data: JSON.stringify({'position': position, 'path': path}),
        method: "POST",
        contentType: "application/json",
        success: function (result) {
            console.log(result);
            refresh_positions();
            $('#myModal').modal('hide');
        }
    });
});

$('#btn_start').click(function () {
    $.ajax(url + "restart", {
        method: "GET",
        contentType: "application/json",
        success: function (result) {
            console.log(result);
        }
    });
});

$('#btn_stop').click(function () {
    $.ajax(url + "stop", {
        method: "GET",
        contentType: "application/json",
        success: function (result) {
            console.log(result);
        }
    });
});



