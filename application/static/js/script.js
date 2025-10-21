let status= 1

function onGetFile(el) {
 var file = el. files[0]

 var options = { inWrapper: false, ignoreWidth: true, ignoreHeight: true }
 docx.renderAsync(file, document.getElementById("container"), null, options)
   .then(x => console.log("docx: finished"));
}

function theme(div,btn){
	var container=getbyId(div);
	var toogle=getbyId(btn).innerHTML;

	if(toogle=="Light Theme ◑"){
		// transition: filter 2.5s ease-in-out;
		container.setAttribute("class", "light_theme")
		sessionStorage.removeItem("theme");
		sessionStorage.setItem("theme", "light_theme");
		getbyId(btn).innerHTML="Dark Theme &#9681;";
		
	}else if(toogle=="Dark Theme ◑"){
		container.setAttribute("class", "dark_theme")
		sessionStorage.removeItem("theme");
		sessionStorage.setItem("theme", "dark_theme");
		getbyId(btn).innerHTML="Light Theme &#9681;";
		
	}
}

function activaTab(tab){
  $('.nav-tabs a[open_doc_ordhref="#' + tab + '"]').tab('show');
};

function hideShow(id) {
    var id = getbyId(id);
    if(id.style.display != 'block') {
        id.style.display = 'block';
    }else {
        id.style.display = 'none';
    }
}

function getbyId(id){
	var rd=document.getElementById(id);
	return rd
}

function clearAll(data) {
    var dataArr = data.split(',');
    for(var i = 0; i <dataArr.length; i++) {
        var id =  getbyId(dataArr[i]);
        if(id) {    
            if(id.tagName.toLocaleLowerCase() == 'input' || id.tagName.toLocaleLowerCase() == 'textarea' || id.tagName.toLocaleLowerCase() == 'select') {
                id.value="";
            }else {
                id.innerHTML = "";
            }
        }else {
            console.log('id not found');
        }
    }
}


function saved(message){
	Swal.fire({
	  position: 'middle',
	  icon: 'success',
	  title: message,
	  showConfirmButton: false,
	  timer: 1500,
	  customClass: 'swal_css'
	})
}

function inform(message){
	Swal.fire({
	  position: 'middle',
	  icon: 'info',
	  title: message,
	  showConfirmButton: false,
	  timer: 1500,
	  customClass: 'swal_css'
	})
}

function topRightAlert(message){
	Swal.fire({
		position: "top-end",
		title: message,
		showConfirmButton: false,
		timer: 3000,
		footer: 'results found',
		showClass: {
			popup: 'animate__animated animate__fadeInDown'
		},
		hideClass: {
			popup: 'animate__animated animate__fadeOutUp'
		}
	});
}

function fade(message){
	Swal.fire({
	  title: message,
	  icon:'info',
	  showClass: {
	    popup: 'animate__animated animate__fadeInDown'
	  },
	  hideClass: {
	    popup: 'animate__animated animate__fadeOutUp'
	  }
	})
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

function send_load_data(){
	swal.fire({
	  title: "Sending Data",
	  text: "Submiting data request",
	  type: "info",
	  showCancelButton: true,
	  showLoaderOnConfirm: true,
	  preConfirm: () => {
	    return fetch(console.log("dsfds"))
	    .then()
	    .catch(() => {
	        Swal.fire({
	          icon: 'error',
	          title: 'Error occured'
	        })
	    })
	  }
	})
}

function warning(message){
	Swal.fire({
	  icon: 'warning',
	  title: message,
	  text: '',
	  customClass: 'swal_css',
	  footer: '<a href>Why do I have this issue?</a>'
	})
}


async function upload_modal(){
	const { value: file } = await Swal.fire({
	  title: 'Select image',
	  input: 'file',
	  inputAttributes: {
	    'accept': 'image/*',
	    'aria-label': 'Upload your profile picture'
	  }
	})

	if (file) {
	  const reader = new FileReader()
	  reader.onload = (e) => {
	    Swal.fire({
	      title: 'Your uploaded picture',
	      imageUrl: e.target.result,
	      imageAlt: 'The uploaded picture'
	    })
	  }
	  reader.readAsDataURL(file)
	}
}


var mydragg = function(){
    return {
        move : function(divid,xpos,ypos){
            divid.style.left = xpos + 'px';
            divid.style.top = ypos + 'px';
        },
        startMoving : function(divid,container,evt){
            evt = evt || window.event;
            var posX = evt.clientX,
                posY = evt.clientY,
            divTop = divid.style.top,
            divLeft = divid.style.left,
            eWi = parseInt(divid.style.width),
            eHe = parseInt(divid.style.height),
            cWi = parseInt(getbyId(container).style.width),
            cHe = parseInt(getbyId(container).style.height);
            getbyId(container).style.cursor='move';
            divTop = divTop.replace('px','');
            divLeft = divLeft.replace('px','');
            var diffX = posX - divLeft,
                diffY = posY - divTop;
            document.onmousemove = function(evt){
                evt = evt || window.event;
                var posX = evt.clientX,
                    posY = evt.clientY,
                    aX = posX - diffX,
                    aY = posY - diffY;
                    if (aX < 0) aX = 0;
                    if (aY < 0) aY = 0;
                    if (aX + eWi > cWi) aX = cWi - eWi;
                    if (aY + eHe > cHe) aY = cHe -eHe;
                mydragg.move(divid,aX,aY);
            }
        },
        stopMoving : function(container){
            var a = document.createElement('script');
            getbyId(container).style.cursor='default';
            document.onmousemove = function(){}
        },
    }
}();

var a = ['','one ','two ','three ','four ', 'five ','six ','seven ','eight ','nine ','ten ','eleven ','twelve ','thirteen ','fourteen ','fifteen ','sixteen ','seventeen ','eighteen ','nineteen '];
var b = ['', '', 'twenty','thirty','forty','fifty', 'sixty','seventy','eighty','ninety'];
function inWords (num) {
    if ((num = num.toString()).length > 9) return 'overflow';
    n = ('000000000' + num).substr(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
    if (!n) return; var str = '';
    str += (n[1] != 0) ? (a[Number(n[1])] || b[n[1][0]] + ' ' + a[n[1][1]]) + 'crore ' : '';
    str += (n[2] != 0) ? (a[Number(n[2])] || b[n[2][0]] + ' ' + a[n[2][1]]) + 'lakh ' : '';
    str += (n[3] != 0) ? (a[Number(n[3])] || b[n[3][0]] + ' ' + a[n[3][1]]) + 'thousand ' : '';
    str += (n[4] != 0) ? (a[Number(n[4])] || b[n[4][0]] + ' ' + a[n[4][1]]) + 'hundred ' : '';
    str += (n[5] != 0) ? ((str != '') ? 'and ' : '') + (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) + 'PESOS ' : '';
    return str;
}

function select_remove_value_where(id,value){
	var selectobject = document.getElementById(id);
    for (var i=0; i<selectobject.length; i++) {
        if (selectobject.options[i].value == value)
            selectobject.remove(i);
    }
}

function showModal(div){
	$('#'+div).show().addClass('modal-open');
}

function download_file(elem) {
	alert(elem.getAttribute('data-path'))

}

function delete_file(elem){
	var data={
		ordinance_file_id:elem.getAttribute('data-id')
	}
	Swal.fire({
		title: 'Are you sure?',
		text: "You won't be able to revert this!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#d33',
		cancelButtonColor: '#3085d6',
		confirmButtonText: 'Yes, delete it!',
		customClass: 'swal_css',
	}).then((result) => {
		if (result.isConfirmed) {
			Swal.fire(
			  'Deleted!',
			  'Your file has been deleted.',
			  'success'
			)
			sendDataWithCallback('/delete_ordinance_file',data,function(res){
				if(res){
					$('#tbl_add_ordinance_file').DataTable().destroy();
					var data={
		        		ordinance_id:elem.getAttribute('data-ordinance_id')
		        	}

					load_ordinance_file(data)
				}
			})
		}
	})
	
}

function delete_file_res(elem){
	var data={
		resolution_file_id:elem.getAttribute('data-id')
	}
	Swal.fire({
		title: 'Are you sure?',
		text: "You won't be able to revert this!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#d33',
		cancelButtonColor: '#3085d6',
		confirmButtonText: 'Yes, delete it!',
		customClass: 'swal_css',
	}).then((result) => {
		if (result.isConfirmed) {
			Swal.fire(
			  'Deleted!',
			  'Your file has been deleted.',
			  'success'
			)
			sendDataWithCallback('/delete_resolution_file',data,function(res){
				if(res){
					$('#tbl_res_attach_file').DataTable().destroy();
					var data={
		        		resolution_id:elem.getAttribute('data-resolution_id')
		        	}
		        	
					load_resolution_file_attach(data)
				}
			})
		}
	})
	
}


// function delete_file_minutes2(elem){
// 	var data={
// 		ordinance_file_committee_id:elem.getAttribute('data-id')
// 	}
// 	Swal.fire({
// 		title: 'Are you sure?',
// 		text: "You won't be able to revert this!",
// 		icon: 'warning',
// 		showCancelButton: true,
// 		confirmButtonColor: '#d33',
// 		cancelButtonColor: '#3085d6',
// 		confirmButtonText: 'Yes, delete it!',
// 		customClass: 'swal_css',
// 	}).then((result) => {
// 		if (result.isConfirmed) {
// 			Swal.fire(
// 			  'Deleted!',
// 			  'Your file has been deleted.',
// 			  'success'
// 			)
// 			sendDataWithCallback('/delete_minutes_file',data,function(res){
// 				if(res){
// 					$('#tbl_add_ordinance_file').DataTable().destroy();
// 					var data={
// 		        		ordinance_id:elem.getAttribute('data-ordinance_id')
// 		        	}
// 					load_committe_ref_file(data)
// 				}
// 			})
// 		}
// 	})
	
// }

function load_resolution_file(data){
	sendDataWithCallback('/get_resolution_file',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-ordinance_id="+ file.ordinance_id+ " data-id=" + file.ordinance_file_id+ " onclick=delete_file_res(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})
			if ($.fn.DataTable.isDataTable('#tbl_add_ordinance_file')) {
	        	$('#tbl_add_ordinance_file').DataTable().destroy();
	       	}

			var table=$('#tbl_add_ordinance_file').DataTable({
                data:res,
                 columns: [
                 	{data:"filename"},
                 	{data: "action"}
                 ],
                responsive: true,
                searching: false, paging: false, info: false


            });
		}
	})
}

function load_ordinance_file(data){
	sendDataWithCallback('/get_ordinance_file',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-ordinance_id="+ file.ordinance_id+ " data-id=" + file.ordinance_file_id+ " onclick=delete_file(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})
			if ($.fn.DataTable.isDataTable('#tbl_add_ordinance_file')) {
	        	$('#tbl_add_ordinance_file').DataTable().destroy();
	       	}

			var table=$('#tbl_add_ordinance_file').DataTable({
                data:res,
                 columns: [
                 	{data:"filename"},
                 	{data: "action"}
                 ],
                responsive: true,
                searching: false, paging: false, info: false


            });
		}
	})
}

function delete_ordinance_vetofile(elem){
	var data={
		veto_ordinance_id:elem.getAttribute('data-veto_ordinance_id'),
		ordinance_id:elem.getAttribute('data-ordinance_id')
	}
	Swal.fire({
		title: 'Are you sure?',
		text: "You won't be able to revert this!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#d33',
		cancelButtonColor: '#3085d6',
		confirmButtonText: 'Yes, delete it!',
		customClass: 'swal_css',
	}).then((result) => {
		if (result.isConfirmed) {
			Swal.fire(
			  'Deleted!',
			  'Your file has been deleted.',
			  'success'
			)
			sendDataWithCallback('/delete_veto_ordinance_file',data,function(res){
				if ($.fn.DataTable.isDataTable('#tbl_veto_ordinance')) {
					$('#tbl_veto_resolution').DataTable().clear().draw();
				}
				load_ordinance_veto_file(data)
				Swal.fire(
				  'Deleted!',
				  'Your file has been deleted.',
				  'success'
				)
			})
		}
	})
}

// function delete_resolution_vetofile(elem){
// 	var data={
// 		veto_resolution_id:elem.getAttribute('data-veto_resolution_id'),
// 		resolution_id:elem.getAttribute('data-resolution_id')
// 	}
// 	Swal.fire({
// 		title: 'Are you sure?',
// 		text: "You won't be able to revert this!",
// 		icon: 'warning',
// 		showCancelButton: true,
// 		confirmButtonColor: '#d33',
// 		cancelButtonColor: '#3085d6',
// 		confirmButtonText: 'Yes, delete it!',
// 		customClass: 'swal_css',
// 	}).then((result) => {
// 		if (result.isConfirmed) {
// 			sendDataWithCallback('/delete_veto_resolution_file',data,function(res){
// 				if(res){
// 					$('#tbl_veto_resolution').DataTable().destroy();
// 					load_resolution_veto_file(data)
// 					Swal.fire(
// 					  'Deleted!',
// 					  'Your file has been deleted.',
// 					  'success'
// 					)
// 				}
// 			})
// 		}
// 	})
// }

function load_ordinance_veto_file(data){
	sendDataWithCallback('/get_ordinance_veto_file',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-ordinance_id="+ file.ordinance_id+ " data-veto_ordinance_id=" + file.veto_ordinance_id+ " onclick=delete_ordinance_vetofile(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})
			if ($.fn.DataTable.isDataTable('#tbl_veto_ordinance')) {
	        	$('#tbl_veto_ordinance').DataTable().destroy();
	       	}

			var table=$('#tbl_veto_ordinance').DataTable({
                data:res,
                 columns: [
                 	{data:"filename"},
                 	{data: "action"}
                 ],
                responsive: true,
                searching: false, paging: false, info: false


            });
		}
	})
}

function load_resolution_veto_file(data){
	sendDataWithCallback('/get_resolution_veto_file',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-resolution_id="+ file.resolution_id+ " data-veto_resolution_id=" + file.veto_resolution_id+ " onclick=delete_resolution_vetofile(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})
			if ($.fn.DataTable.isDataTable('#tbl_veto_resolution')) {
	        	$('#tbl_veto_resolution').DataTable().destroy();
	       	}

			var table=$('#tbl_veto_resolution').DataTable({
                data:res,
                 columns: [
                 	{data:"filename"},
                 	{data: "action"}
                 ],
                responsive: true,
                searching: false, paging: false, info: false


            });
		}
	})
}

function load_committe_ref_file(data){
	sendDataWithCallback('/get_committe_ord_file',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-ordinance_id="+ file.ordinance_id+ " data-id=" + file.ordinance_file_committee_id + " onclick=delete_file_minutes2(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})
			if ($.fn.DataTable.isDataTable('#tbl_add_minutes_file')) {
	        	$('#tbl_add_minutes_file').DataTable().destroy();
	       	}


			var table=$('#tbl_add_minutes_file').DataTable({
                data:res,
                 columns: [
                 	{data:"filename"},
                 	{data: "action"}
                 ],
                responsive: true,
                searching: false, paging: false, info: false
            });
		}
	})
}

function title_string(string) 
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function readURL(input,img) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#'+img)
      .attr('src', e.target.result)
      .width(200)
      .height(200);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


function readURL_full(input,img) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#'+img)
      .attr('src', e.target.result)
      // .width(200)
      // .height(200);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


function loadfirstdatatable(tbl){
	$('#'+tbl).DataTable({
        data:null,
        responsive: true,
        dom: 'ftipr',
        paging:false,
        searching:false,
        "showNEntries" : false
    });
}

function load_resolution_minutes_file(min_data){
	sendDataWithCallback('/get_minutes_file_resolution', min_data, function(res) {
		if ($.fn.DataTable.isDataTable('#tbl_add_minutes_file_resolution')) {
			$('#tbl_add_minutes_file_resolution').DataTable().clear().destroy(); // Destroy instead of just clearing
		}
	
		if (res.length > 0 && res[0].minutes_res_id != null) {
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-minutes_id='" + file.minutes_id + "' data-minutes_res_id='" + file.minutes_res_id + "' onclick='delete_resolution_minutes_file(this)'> DELETE </button>";
				var dl_btn = "<a data-path='" + file.path + "' href='/static/uploads/" + file.path + "'><button type='button'> DOWNLOAD </button></a>";
				file.action = dl_btn + del_btn;
			});
	
			$('#tbl_add_minutes_file_resolution').DataTable({
				data: res,
				columns: [
					{ data: "filename" },
					{ data: "action" }
				],
				responsive: true,
				searching: false,
				paging: false,
				info: false
			});
		}
	});
	
}

function delete_resolution_minutes_file(datas){
	Swal.fire({
	  title: 'Are you sure?',
	  text: "You won't be able to revert this!",
	  icon: 'warning',
	  showCancelButton: true,
	  confirmButtonColor: '#d33',
	  cancelButtonColor: '#3085d6',
	  confirmButtonText: 'Yes, delete it!',
	  customClass: 'swal_css',
	}).then((result) => {
		if (result.isConfirmed) {
			Swal.fire(
			  'Deleted!',
			  'Your file has been deleted.',
			  'success'
			)
			sendDataWithCallback('/delete_resolution_minutes_file',data = {
				minutes_res_id: datas.getAttribute('data-minutes_res_id'),
				minutes_id: datas.getAttribute('data-minutes_id'),
			},function(res){
				var min_data={
					minutes_id: datas.getAttribute('data-minutes_res_id')
				}

				console.log(min_data, "min_data ????")
				load_resolution_minutes_file(min_data)
			})
		}
	})
}


function show_spinner(){
  getbyId("spinner-back").classList.add("show");
  getbyId("spinner-front").classList.add("show");
}
function hide_spinner(){
  getbyId("spinner-back").classList.remove("show");
  getbyId("spinner-front").classList.remove("show");
}

function show_spinner2(){
  // getbyId("spinner-back2").classList.add("show");
  // getbyId("spinner-front2").classList.add("show");
}

function hide_spinner2(){
  // getbyId("spinner-back2").classList.remove("show");
  // getbyId("spinner-front2").classList.remove("show");
}


function printer(to_print_id){
	printJS({printable:to_print_id,type: 'html',css: ['../static/css/style.css','../static/css/bootstrap.min.css',
		'../static/css/dataTables.bootstrap.css','../static/css/jquery.dataTables.min.css'],style:'p{padding:0px!important;margin:0px!important};hr { margin: 3px; }:root{filter: invert(0%);};',scanStyles:false,onError: function  (error) {
		alert('Error found => ' + error.message)
		}
	})
}

function printer_landscape(to_print_id){
	printJS({printable:to_print_id,type: 'html',css: ['../static/css/style.css','../static/css/bootstrap.min.css',
		'../static/css/dataTables.bootstrap.css','../static/css/jquery.dataTables.min.css'],honorMarginPadding:false ,style: '@page { size: Letter landscape; }:root{filter: invert(0%);};}',scanStyles:false,onError: function  (error) {
		alert('Error found => ' + error.message)
		}
	})
}

function doc_tracking_reso(){
	getDataWithCallback('/get_track_document_reso', function(res){
		if ($.fn.DataTable.isDataTable('#tbl_document_traking')) {
            $('#tbl_document_traking').DataTable().destroy();
        }
        var table=$('#tbl_document_traking').DataTable({
            data:res,
            columns: [
                {data:"resolution_id"},
                {data:"resolution_number"},
                {data:"resolution_title"},
                {data:"committee"},
                {data:"stats"},
                {data:"type_document"},
                {data:"date_enacted"},
            ],
             buttons: [
                {
                    extend: 'print',
                    text: 'Print',
                    filename: 'file',
                    title: 'Print',
                    titleAttr: 'Print'
                    ,'className': 'btn btn-warning'
                }
            ],
            dom: 'Bfrtip',
            responsive: true,
            "pagingType": "full_numbers",
            "bInfo": false,
            searching:true,
            pageLength: 3,
        });

        $('#tbl_document_traking tbody').on('dblclick', 'tr', function (){
        	var dataArr = $('#tbl_document_traking').DataTable().row( this ).data();

        	getbyId('document_id').value=dataArr['resolution_id']

        	getbyId('document_type').value="RESOLUTION"

        	$("#div_modal_track").modal('show')
	    })
	})


}

function get_res_ord_pet(typ){
    if ($.fn.DataTable.isDataTable('#tbl_document_traking')) {
        $('#tbl_document_traking').DataTable().clear().draw();
    }

    if(typ==1){
        doc_tracking_reso()
    }else if(typ==2){
        getDataWithCallback('/get_track_document_ord', function(res){
			if ($.fn.DataTable.isDataTable('#tbl_document_traking')) {
                $('#tbl_document_traking').DataTable().destroy();
            }
            var table=$('#tbl_document_traking').DataTable({
                data:res,
                columns: [
                    {data:"ordinance_id"},
                    {data:"ordinance_number"},
                    {data:"ordinance_title"},
                    {data:"committee"},
                    {data:"stats"},
                    {data:"type_document"},
                    {data:"date_enacted"},
                ],
                 buttons: [
                    {
                        extend: 'print',
                        text: 'Print',
                        filename: 'file',
                        title: 'Print',
                        titleAttr: 'Print'
                        ,'className': 'btn btn-warning'
                    }
                ],
                dom: 'Bfrtip',
                responsive: true,
                "pagingType": "full_numbers",
                "bInfo": false,
                searching:true,
                pageLength: 3,
            });

            $('#tbl_document_traking tbody').on('dblclick', 'tr', function (){
	        	var dataArr = $('#tbl_document_traking').DataTable().row( this ).data();

	        	getbyId('document_id').value=dataArr['ordinance_id']
	        	getbyId('document_type').value="ORDINANCE"

	        	$("#div_modal_track").modal('show')
		    })
		})
    }else if(typ==3){
        getDataWithCallback('/get_track_document_pet', function(res){
			if ($.fn.DataTable.isDataTable('#tbl_document_traking')) {
                $('#tbl_document_traking').DataTable().destroy();
            }
            var table=$('#tbl_document_traking').DataTable({
                data:res,
                columns: [
                    {data:"petition_id"},
                    {data:"title"},
                    {data:"committee"},
                    {data:"stats"},
                    {data:"type_document"},
                    {data:"date_petetion"},
                ],
                 buttons: [
                    {
                        extend: 'print',
                        text: 'Print',
                        filename: 'file',
                        title: 'Print',
                        titleAttr: 'Print'
                        ,'className': 'btn btn-warning'
                    }
                ],
                dom: 'Bfrtip',
                responsive: true,
                "pagingType": "full_numbers",
                "bInfo": false,
                searching:true,
                pageLength: 3,
            });

            $('#tbl_document_traking tbody').on('dblclick', 'tr', function (){
	        	var dataArr = $('#tbl_document_traking').DataTable().row( this ).data();

	        	getbyId('document_id').value=dataArr['petition_id']
	        	getbyId('document_type').value="PETETION"
	        	
	        	$("#div_modal_track").modal('show')
		    })

		})
    }
}

/* reports */

function get_res_ord_pet_reports(typ){
    if ($.fn.DataTable.isDataTable('#tbl_document_traking_reports')) {
        $('#tbl_document_traking_reports').DataTable().clear().draw();
    }
    $('#inp_report_tracker').empty();

     sendDataWithCallback("/get_report_integrated", {type: typ} ,function(res){
        if(res){
             $('#inp_report_tracker').chosen({width:"100%"})
            $('#inp_report_tracker').append(`<option value="" disabled selected> ${'--SELECT--'} </option>`);
            for(var x=0; x<res.length; x++){
                $('#inp_report_tracker').append(`<option value="${res[x].tracking_no}"> ${res[x].title} (tracking#${res[x]['tracking_no']}) </option>`);
            }
            $('#inp_report_tracker').trigger("chosen:updated")
        }
    })
}

function get_track_document_reports(data_id,type){
    var data={
        tracking_no:data_id
    }

    sendDataWithCallback('/get_tracking_document_report',data,function(res){
        if(res[0]){
            if ($.fn.DataTable.isDataTable('#tbl_document_traking_reports')) {
                $('#tbl_document_traking_reports').DataTable().destroy();
            }

            var table=$('#tbl_document_traking_reports').DataTable({
                data:res,
                 columns: [
                    {data:"tracking_no"},
                    {data:"title"},
                    {data:"committee", "render": function (data, type, row) {if (row.committee==null) {return 'n/a'}else{ return row.committee}} },
                    {data:"status"},
                    {data:"type_document"},
                    {data:"date"},
                ],
                dom: 'ftipr',
                responsive: true,
                "paging":false,
                "bInfo": false,
                searching:false,
                "showNEntries" : false
            }); 
        }
    })
}

/* end reports */


function get_track_document(data_id,type){
    var data={
        typ:type,
        id:data_id
    }

    sendDataWithCallback('/get_track_document_logs',data,function(res){
        if(res[0]){
            if ($.fn.DataTable.isDataTable('#tbl_document_traking')) {
                $('#tbl_document_traking').DataTable().destroy();
            }
            var table=$('#tbl_document_traking').DataTable({
                data:res,
                columns: [
                    {data:"track_gen_id"},
                    {data:"title"},
                    {data:"committee"},
                    {data:"stats"},
                    {data:"type_document"},
                    {data:"date"},
                ],
                buttons: [
                    {
                        extend: 'print',
                        text: 'Print',
                        filename: 'file',
                        title: 'Print',
                        titleAttr: 'Print'
                        ,'className': 'btn btn-warning prnt_top'
                    }
                ],
                dom: 'Bfrtip',
                responsive: true,
                "pagingType": "full_numbers",
                "bInfo": false,
                searching:true,
                pageLength: 3,
            }); 
        }
    })
}


function numberWithCommas(x) {
	if(x==null || x==""){
		return 0
	}else{
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")+".00";
	}
   
}

function numberWithCommas_no_decimal(x) {
	if(x==null || x==""){
		return 0
	}else{
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}
   
}

function load_resolution_file_attach(data){
	sendDataWithCallback('/get_resolution_file2',data,function(res){
		if(res){
			res.forEach(function(file) {
				var del_btn = "<button type='button' data-resolution_id="+ file.resolution_id+ " data-resolution_file_id=" + file.resolution_file_id+ " onclick=del_resolution_file_attach(this)> DELETE </button>"
				var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
				file.action = dl_btn + del_btn ;
			})

			if ($.fn.DataTable.isDataTable('#tbl_res_attach_file')) {
	        	$('#tbl_res_attach_file').DataTable().destroy();
	       	}
			var table=$('#tbl_res_attach_file').DataTable({
	            data:res,
	             columns: [
	             	{data:"filename"},
	             	{data: "action"}
	             ],
	            responsive: true,
	            searching: false, paging: false, info: false
	        });
		}

		var min_data={
			minutes_id:getbyId('h_resolution_id').value
		}
		load_resolution_minutes_file(min_data)
	})
}


function open_doc_res(elem, tbl) {
    var tr = $(elem).closest('tr')
    var dataArr = $(tbl).DataTable().row(tr).data()

    $("#inp_committee_res").val([]).trigger("chosen:updated");
    if(dataArr){
 		getbyId('h_committee_id_res').value=dataArr.resolution_id

 		var data={
 			resolution_id:dataArr.resolution_id
 		}

 		getbyId('status_resolution').disabled=false
 		sendDataWithCallback('/get_resolution_file',data,function(res){
 			if(res){
 				getbyId('btn_resolution_committee').style.display="block"
 				getbyId('h_resolution_id').value=dataArr.resolution_id
 				getbyId('tracking_no_res').value=res[0].tracking_number
 				getbyId('sel_ordinance_classification_res').value=res[0].classification_id
 				// getbyId('sel_ordinance_category_res').value=res[0].category

 				var split_category= []
	    		if(res[0].category){
		    		split_category = res[0].category.split(",")
		    		$("#sel_ordinance_category_res").val(split_category).trigger("chosen:updated");
		    	}
	    	
 				getbyId('resolution_no').value=res[0].resolution_number
 				getbyId('resolution_title').value=res[0].resolution_title
 				getbyId('resolution_author').value=res[0].author
 				getbyId('date_enacted_res').value=res[0].date_enacted

 				$('#inp_sp_ord_legislature_res').val(res[0].sp_id).trigger('chosen:updated')
   				
        		var splits= []

	    		if(dataArr.ref_committee){
		    		splits = dataArr.ref_committee.split(",")
		    		$("#inp_committee_res").val(splits).trigger("chosen:updated");
		    	}

 				getbyId('resolution_series_number').value=res[0].series_number
 				getbyId('inp_session_res').value=res[0].session_id
 				getbyId('sel_source_docs_res').value=res[0].source_of_document
 				getbyId('remarks_res').value=res[0].remarks
 				getbyId('h_committee_id_res').value=res[0].committee_id
 				getbyId('h_legislature_res').value=res[0].sp_id
 				getbyId('minutes_resolution').value=res[0].minutes_title

 				if(res[0].minutes_ids){
 					getbyId('resolution_minutes_id').value=res[0].minutes_ids
 				}else{
 					getbyId('resolution_minutes_id').value=0
 				}

 				var text = ""
	     		if(res[0].description == null || res[0].description == "") {
	     			text="NO DESCRIPTION"
	     		}else{
	     			text = res[0].description
	     		}
	     		tinymce.get("tx_description_res").setContent(text);
     			}

     			getbyId('status_resolution').value=res[0].status
     			
     			sendDataWithCallback('/get_resolution_file2',data,function(res){
					if(res){
						res.forEach(function(file) {
							var del_btn = "<button type='button' data-resolution_id="+ file.resolution_id+ " data-id=" + file.resolution_file_id+ " onclick=delete_file_res(this)> DELETE </button>"
							var dl_btn = "<a data-path=" +file.path+ " href=" + '/static/uploads/'+file.path+ "><button type='button'> DOWNLOAD </button></a>"
							file.action = dl_btn + del_btn ;
						})

						if ($.fn.DataTable.isDataTable('#tbl_res_attach_file')) {
				        	$('#tbl_res_attach_file').DataTable().destroy();
				       	}
						var table=$('#tbl_res_attach_file').DataTable({
			                data:res,
			                 columns: [
			                 	{data:"filename"},
			                 	{data: "action"}
			                 ],
			                responsive: true,
			                searching: false, paging: false, info: false
			            });
					}

					var min_data={
						minutes_id:getbyId('h_resolution_id').value
					}
					
					load_resolution_minutes_file(min_data)
					load_resolution_veto_file(data)
				})
 		})

 		count_authors=0
			sendDataWithCallback('/get_author_resolutions',data,function(res){
				getbyId('div_resolution_author').innerHTML="";
            res.forEach(function(i,index){
                add_res_author(function(sel) {
                    sel.value = i['author']
                    $(sel).trigger('chosen:updated');
                });
            })
 		})

			count_co_authors=0
		sendDataWithCallback('/get_co_author_resolutions',data,function(res){
			getbyId('div_resolution_co_author').innerHTML="";
            res.forEach(function(i,index){
                add_res_co_author(function(sel) {
                    sel.value = i['co_author']
                    $(sel).trigger('chosen:updated');
                });
            })
 		})

		count_sponsor=0
 		sendDataWithCallback('/get_sponsor_resolutions',data,function(res){
 			getbyId('div_resolution_sponsor').innerHTML="";
            res.forEach(function(i,index){
                add_res_sponsor(function(sel) {
                    sel.value = i['sponsor']
                    $(sel).trigger('chosen:updated');
                });
            })
 		})
 		
 		$("#div_resolution_modal").modal('toggle');
 	}
}


function open_doc_ord(elem, tbl){
	var tr = $(elem).closest('tr')
	
	var dataArr = $(tbl).DataTable().row(tr).data()
	console.log(dataArr, "dataArr.ref_committee")
	getbyId('form_ordinance').reset();

	getbyId('status_ordinance').disabled=false;

	$("#inp_committee_ordinance").val([]).trigger("chosen:updated");

	var forms = getbyId('form_ordinance')

	if(dataArr){
    	getbyId('btn_ordinance_committee').style.display="block"
    	getbyId('h_ordinance_id').value=dataArr.ordinance_id;

    	var data={
    		ordinance_id:dataArr.ordinance_id
    	}

    	forms.type_ord.value= dataArr['type_ord']

    	sendDataWithCallback('/get_ordinance_by_status',data,function(res){
    		getbyId('status_ordinance').value=res[0].status
    		getbyId('tracking_no_ord').value=res[0].tracking_number
    		getbyId('sel_ordinance_classification').value=res[0].classification_id

    		getbyId('h_committee_id_ord').value=res[0].committee_id

    		var split_category= []
    		if(res[0].category){
	    		split_category = res[0].category.split(",")
	    		$("#sel_ordinance_category").val(split_category).trigger("chosen:updated");
	    	}

    		getbyId('ordinance_no').value=res[0].ordinance_number
    		getbyId('date_enacted_ord').value=res[0].date_enacted
    		getbyId('ordinance_title').value=res[0].ordinance_title
    		getbyId('h_sp_legislature').value=res[0].sp_id

    		$('#inp_sp_ord_legislature').val(res[0].sp_id).trigger('chosen:updated')
    		
    		var splits= []


    		if(dataArr.ref_committee){
	    		splits = dataArr.ref_committee.split(",")
	    		$("#inp_committee_ordinance").val(splits).trigger("chosen:updated");
	    	}

    		getbyId('inp_session_ordinance').value=res[0].session_id

    		getbyId('sel_source_docs').value=res[0].source_of_document
    		getbyId('sel_source_docs').dispatchEvent(new Event('change'));
    		getbyId('source_document_specify').value=res[0].source_document_specify


    		getbyId('series_number').value=res[0].series_number

    		if(res[0].ammended_no=="" || res[0].ammended_no==null){
    			getbyId('amended_ord').checked=false
    		}else{
    			getbyId('amended_no_ord').value=res[0].ammended_no
    			getbyId('amended_ord').checked=true
    		}

    		if(res[0].repealed_no=="" || res[0].repealed_no==null){
    			getbyId('repealed_ord').checked=false
    		}else{
    			getbyId('repealed_no_ord').value=res[0].repealed_no
    			getbyId('repealed_ord').checked=true
    			
    		}
    		if(res[0].superseded_no=="" || res[0].superseded_no==null){
    			getbyId('supers_ord').checked=false
    		}else{
    			getbyId('supers_no_ord').value=res[0].superseded_no
    			getbyId('supers_ord').checked=true
    		}

    		getbyId('remarks_ord').value=res[0].remarks

    		if(res[0].original=="1"){
    			getbyId('orginal_3_status_ord').checked=true
    		}else{
    			getbyId('orginal_3_status_ord').checked=false
    		}

    		if(res[0].missing_ord=="1"){
    			getbyId('missing_ord').checked=true
    		}

    		var text = ""
     		if(res[0].description == null || res[0].description == "") {
     			text="NO DESCRIPTION"
     		}else{
     			text = res[0].description
     		}

     		tinymce.get("tx_description").setContent(text);

     		getbyId('minutes_ordinance').value=res[0].minutes_title
     		getbyId('ordinance_minutes_id').value=res[0].min_id

    		load_ordinance_file(data)
    		load_committe_ref_file(data)

    		count_authors=0
 			sendDataWithCallback('/get_author_ordinances',data,function(res){
 				getbyId('div_ordinance_author').innerHTML="";
                res.forEach(function(i,index){
                    add_ord_author(function(sel) {
                        sel.value = i['author']
                        $(sel).trigger('chosen:updated');
                    });
                })

     		})

 			count_co_authors=0
			sendDataWithCallback('/get_co_author_ordinance',data,function(res){
				getbyId('div_ordinance_co_author').innerHTML="";
  				res.forEach(function(i,index){
                    add_ord_co_author(function(sel) {
                        sel.value = i['co_author']
                        $(sel).trigger('chosen:updated');
                    });
                })
     		})

			count_sponsor=0
     		sendDataWithCallback('/get_sponsor_ordinance',data,function(res){
     			getbyId('div_ordinance_sponsor').innerHTML="";
  				res.forEach(function(i,index){
                    add_ord_sponsor(function(sel) {
                        sel.value = i['sponsor']
                        $(sel).trigger('chosen:updated');
                    });
                })
     		})

    	})

    	load_ordinance_veto_file(data)

        $('#div_add_ordinance').modal('toggle');    
    }
}


function get_gov_classification(){
	getDataWithCallback('/get_gov_classification',function(res){
		$('#sel_ordinance_classification').append(`<option value="" disabled selected> ${'--SELECT--'} </option>`);
		for(var x=0; x<res.length; x++){
			$('#sel_ordinance_classification').append(`<option value="${res[x]['classification_id']}"> ${res[x]['title']} </option>`); 
		}
	})
}

function get_category(){
	$('#sel_classification_category').chosen({allow_single_deselect: true})
	$('#sel_classification_category').append(`<option value="" disabled selected> ${'--SELECT--'} </option>`);
	getDataWithCallback('/get_category',function(res){ 
		for(var x=0; x<res.length; x++){ 
			$('#sel_ordinance_category').append(`<option value="${res[x]['category_id']}"> ${res[x]['title']} </option>`);
			$('#sel_classification_category').append(`<option value="${res[x]['category_id']}"> ${res[x]['title']} </option>`);
		}

		$('#sel_ordinance_category').trigger('chosen:updated')
		$('#sel_classification_category').trigger('chosen:updated')
	})
}



function openWordFile(fileUrl) {
    fetch(fileUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error("File not found or inaccessible.");
            }
            return response.arrayBuffer();
        })
        .then(arrayBuffer => {
            return mammoth.convertToHtml({ arrayBuffer });
        })
        .then(result => {
            const htmlContent = result.value;

            const newWindow = window.open('', '_blank');
            if (newWindow) {
                newWindow.document.write('<html><head><title>Converted Word Document</title><style>');
                newWindow.document.write('body { font-family: Arial, sans-serif; margin: 0; padding: 0; height: 100vh; display: flex; justify-content: center; background-color: #f4f4f4; }');
                newWindow.document.write('.content { width: 80%; max-width: 900px; padding: 40px 20px 20px 20px; background-color: white; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); overflow-y: auto; margin-top: 20px; }');
                newWindow.document.write('</style></head><body>');
                newWindow.document.write('<div class="content">');
                newWindow.document.write(htmlContent);
                newWindow.document.write('</div></body></html>');
                newWindow.document.close();
            }
        })
        .catch(error => {
            console.error("Error loading or converting the Word file:", error);
        });
}


function formatReadableDate(dateStr) {
    const date = new Date(dateStr);
    const options = { month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function isValidSelection(text, value) {
    return text && value && text.toUpperCase() !== '--SELECT--';
}

function formatReadableDate(dateStr) {
    if (!dateStr) return ''; // Return empty string if nothing is selected
    const date = new Date(dateStr);
    if (isNaN(date)) return ''; // Handle "Invalid Date"
    const options = { month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

(function($){
    $.fn.serializeObject = function(){
        var self = this,
            json = {},
            push_counters = {},
            patterns = {
                "validate": /^[a-zA-Z][a-zA-Z0-9_]*(?:\[(?:\d*|[a-zA-Z0-9_]+)\])*$/,
                "key":      /[a-zA-Z0-9_]+|(?=\[\])/g,
                "push":     /^$/,
                "fixed":    /^\d+$/,
                "named":    /^[a-zA-Z0-9_]+$/
            };


        this.build = function(base, key, value){
            base[key] = value;
            return base;
        };

        this.push_counter = function(key){
            if(push_counters[key] === undefined){
                push_counters[key] = 0;
            }
            return push_counters[key]++;
        };
// kani ang guba kay dli makita ang name daan ani na jquery library
        $.each($(this).serializeArray(), function(){

            // Skip invalid keys
            if(!patterns.validate.test(this.name)){
                return;
            }

            var k,
                keys = this.name.match(patterns.key),
                merge = this.value,
                reverse_key = this.name;

            while((k = keys.pop()) !== undefined){

                // Adjust reverse_key
                reverse_key = reverse_key.replace(new RegExp("\\[" + k + "\\]$"), '');

                // Push
                if(k.match(patterns.push)){
                    merge = self.build([], self.push_counter(reverse_key), merge);
                }

                // Fixed
                else if(k.match(patterns.fixed)){
                    merge = self.build([], k, merge);
                }

                // Named
                else if(k.match(patterns.named)){
                    merge = self.build({}, k, merge);
                }
            }

            json = $.extend(true, json, merge);
        });

        return json;
    };
})(jQuery);

