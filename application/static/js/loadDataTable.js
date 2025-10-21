
// var data_url= "http://192.168.1.200:1000"

// var data_url= "http://localhost"

function loadDataTable(tblId, data_uril){
    var tbl_id = '#' + tblId;
    var table = $(tbl_id).DataTable({
       "ajax": {
            "type": "GET",
            "url": data_uril,
            "dataSrc": function(data) {
                console.log(data);
                return data;
            }
        },
        "columnDefs": [
            {
                "targets": [0],
                "visible": false,
                "searchable": false
            }
        ]
        ,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'print',
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true"></span>',
                filename: 'file',
                title: '',
                titleAttr: 'Print'
            },
            {
                extend: 'excel',
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span>',
                filename: 'file',
                title: '',
                titleAttr: 'Export to excel'
            }
        ],
        // "order":[[1,"asc"]],
        "stripeClasses": [],
        paging: true,
        searching: true,
    });
}

function loadDataTable_none(tblId, data_uril){
    var tbl_id = '#' + tblId;
        var table = $(tbl_id).DataTable({
            "ajax": {
                "type": "GET",
                "url": data_uril,
                "dataSrc": function(data) {
                    console.log(data);
                    return data;
                }
            },
            "columnDefs": [
                {
                    "targets": [0],
                    "visible": false,
                    "searchable": false
                }
            ],
            "stripeClasses": [],
            paging: false,
            searching: false,
            "bPaginate": false,
            "bLengthChange": false,
            "bFilter": true,
            "bInfo": false,
            "bAutoWidth": false 
        });
}

function loadDataTable_none_nodata(tblId, data_uril){
    var tbl_id = '#' + tblId;
        var table = $(tbl_id).DataTable({
            data:{},
            "columnDefs": [
                {
                    "targets": [0],
                    "visible": false,
                    "searchable": false
                }
            ],
            "stripeClasses": [],
            paging: false,
            searching: false,
            "bPaginate": false,
            "bLengthChange": false,
            "bFilter": true,
            "bInfo": false,
            "bAutoWidth": false 
        });
}

function loadDataTable_none_nodata_obj(tblId, cols){
    var tbl_id = '#' + tblId;
        var table = $(tbl_id).DataTable({
            data:null,
            columns: cols,
            "columnDefs": [
                {
                    "targets": [0],
                    "visible": false,
                    "searchable": false
                }
            ],
            "stripeClasses": [],
            paging: false,
            searching: false,
            "bPaginate": false,
            "bLengthChange": false,
            "bFilter": true,
            "bInfo": false,
            "bAutoWidth": false 
        });
}


function load_dtable_w_footer(url,data,tbl){
    sendDataWithCallback(url,data,function(res){
        var tbl_id = '#' + tbl;
        var table = $(tbl_id).DataTable({
            data:res,
            "columnDefs": [
                {
                    "targets": [0],
                    "visible": false,
                    "searchable": false
                }
            ],
            "stripeClasses": [],
            paging: true,
            searching: false,
            "bPaginate": false,
            "bLengthChange": false,
            "bFilter": true,
            "bInfo": false,
            "bAutoWidth": false ,
            "footerCallback": function ( row, data, start, end, display ) {
                var api = this.api(), data;
             
                // Remove the formatting to get integer data for summation
                var intVal = function ( i ) {
                    return typeof i === 'string' ?
                        i.replace(/[\$,]/g, '')*1 :
                        typeof i === 'number' ?
                            i : 0;
                };
             
                // Total over all pages
                total = api
                    .column( 5 )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
             
                total1 = api
                    .column( 4 )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );

                 total2 = api
                    .column( 3 )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
             
                // Total over this page

                pageTotal = api
                    .column( 5, { page: 'current'} )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
             
                pageTotal1 = api
                    .column( 4, { page: 'current'} )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );

                pageTotal2 = api
                    .column( 3, { page: 'current'} )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
             
             
                // Update footer
                $( api.column( 5 ).footer() ).html(
                    'Expended Balance'+' '+pageTotal +' '
                );
             
                $( api.column( 4 ).footer() ).html(
                    'Expended'+' '+pageTotal1 +' '
                );

                 $( api.column( 3 ).footer() ).html(
                    'Allocated'+' '+pageTotal2 +' '
                );
            }
        });

         $(tbl_id+ ' tbody').on('dblclick', 'tr', function (){
            var dataArr = table.row( this ).data();
            if(dataArr){
                
            }
        });
    })
}


// function recalc_table_withdata(tbl,cols,datas) {
//     if ($.fn.DataTable.isDataTable(tbl)) {
//         $(tbl).DataTable().destroy();
//     }
//     var table;
//     let prom = new Promise( (resolve, reject)=> {
//         table =  $(tbl).DataTable( {
//             dom: 'Bfrtip',
//             data:datas,
//             columns: cols,
//             buttons: [
//                 {
//                     extend: 'print',
//                     text: '<i class="fa fa-print" aria-hidden="true"></i>',
//                     filename: 'file',
//                     title: '',
//                     titleAttr: 'Print'
//                 }
//             ],
//             responsive: true
//         });
//         resolve(table);
//     })
    
// }