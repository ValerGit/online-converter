$(document).ready(function () {
    var max_fields = 10; //maximum input boxes allowed
    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $(".add_field_button"); //Add button ID

    var x = 1; //initlal text box count
    $(add_button).click(function (e) { //on add input button click
        e.preventDefault();
        if (x < max_fields) { //max input box allowed
            x++; //text box increment
            $(wrapper).append('<p class="text-muted m-b-20 font-13 m-h-20"></p><div class="row"> <div class="col-md-3 "> <select class="form-control select2" name="p_scnt"> <option>Select1</option> <option>Select2</option> </select> </div> <div class="col-md-2 "> <select class="form-control select2"> <option>Select1</option> <option>Select2</option> </select> </div> <div class="col-md-3 "> <select class="form-control select2"> <option>Select1</option> <option>Select2</option> </select> </div> <div class="col-md-3"> <select class="form-control select2"> <option>Select1</option> <option>Select2</option> </select> </div> <button type="button" class="btn btn-danger btn-custom  btn-rounded waves-effect waves-light remove_field"> <h7><i class="ion-minus"></i></h7> </button> </div>');
        }
    });

    $(wrapper).on("click", ".remove_field", function (e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })
});


$(document).ready(function () {
    $('.parallax').parallax();
});


$('#set-dbs').click(function () {
    var from_db = $('#from-db option:selected').val().trim();
    var to_db = $('#to-db option:selected').val().trim();
    if ((to_db == '') || (from_db == '')) {
        swal("Введенные параметры не валидны");
    }
    window.location.href = "/tables-choose/?from=" + from_db + "&to=" + to_db;
});