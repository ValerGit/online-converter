$('#set-dbs').click(function () {
    var from_db = $('#from-db option:selected').val().trim();
    var to_db = $('#to-db option:selected').val().trim();
    if ((to_db == '') || (from_db == '')) {
        swal("Введенные параметры не валидны");
    }
    window.location.href = "/tables-choose/?from=" + from_db + "&to=" + to_db;
});
