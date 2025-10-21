// var data_url= "192.168.3.10:1000"
function sendDataWithCallbackbtn(url, data, btn, callback) {
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        beforeSend: function() {
            console.log("sending");
        },
        complete: function() {
            console.log("done sending");
        },
        success: function(data) {
            callback(data)
        },
        error: function() {
            error_in_saving("error occured in sending to " + url);
        }
    });
}


function getDataWithCallback(url, callback) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            callback(data)
        },
        error: function() {
            error_in_saving("error occured in receiving from" + url);
        }
    });
}

function error_in_saving(message){
    Swal.fire({
      icon: 'error',
      title: message,
      text: '',
      customClass: 'swal_css',
      footer: '<a href>Why do I have this issue?</a>'
    })
}

function sendDataWithCallback(url, data, callback) {
    if(url=="/send_emails"){
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json',
            beforeSend: function() {
                console.log("sending")
                show_spinner()
            },
            complete: function() {
                console.log("done sending");
            },
            success: function(data) {
                hide_spinner()
                callback(data)
            },
            error: function() {
                error_in_saving("error occured in sending to " + url);
            }
        });
    }else{
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json',
            beforeSend: function() {
                console.log("sending")
            },
            complete: function() {
                console.log("done sending");
            },
            success: function(data) {
                callback(data)
            },
            error: function() {
                error_in_saving("error occured in sending to " + url);
            }
        });
    }
    
}

function recalc_table_withdata(tbl, cols, datas) {
    if ($.fn.DataTable.isDataTable(tbl)) {
        $(tbl).DataTable().destroy();
    }
    var table;
    if(tbl=="#tbl_barangay"){
        let prom = new Promise((resolve, reject) => {
            table = $(tbl).DataTable({
                dom: 'Bfrtip',
                data: datas,
                columns: cols,
                buttons: [{
                    text: "<i class='bi bi-plus-square' style='font-size: 1rem; color: white;'></i>",
                    action: function ( e, dt, node, config ) {
                        getbyId('form_barangay').reset();
                        $('#modal_brgy').modal('toggle');
                    },
                    'className': 'btn btn-sm btn-primary'
                },{
                    extend: 'print',
                    text: "<i class='bi bi-printer' style='font-size: 1rem; color: white;'>",
                    filename: 'file',
                    title: '',
                    titleAttr: 'Print',
                    className: 'btn btn-sm btn-warning'
                }],
                responsive: true
            });
            resolve(table);
        })
    }else{
        let prom = new Promise((resolve, reject) => {
            table = $(tbl).DataTable({
                dom: 'Bfrtip',
                data: datas,
                columns: cols,
                buttons: [{
                    extend: 'print',
                    text: "<i class='bi bi-printer' style='font-size: 1rem; color: white;'>",
                    filename: 'file',
                    title: '',
                    titleAttr: 'Print',
                    className: 'btn btn-sm btn-warning'
                }],
                responsive: true
            });
            resolve(table);
        })
    }
    
}

function loadDataIntable(tbl, col, data, modal) {
    if ($.fn.DataTable.isDataTable('#'+tbl)) {
        $('#'+tbl).DataTable().destroy();
    }
    var table = $('#' + tbl).DataTable({
        data: data,
        responsive: true,
        dom: 'Bfrtip',
        columns: col,
        buttons: [{
            text: 'Add New',
            action: function(e, dt, node, config) {
                clear_session_data(function(){
                    populate_active_councilor()
                    populate_code_references()
                    getbyId('btn_del_session').style.display = "none";

                    $("#"+ modal).modal("toggle");

                });
            },
            'className': 'btn btn-success'
        },{
            extend: 'print',
            text: 'Print',
            filename: 'file',
            title: 'Print',
            titleAttr: 'Print'
            ,'className': 'btn btn-warning'
                    } ],
        "pagingType": "full_numbers",
    });
}

var byId = function( id ) { return document.getElementById( id ); };
var createElem = function( id ) { return document.createElement( id ); };