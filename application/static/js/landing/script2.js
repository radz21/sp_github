function show_com(){
	getbyId('sel_committee_propose').style.display = "block";
	getbyId('button_reffer').style.display = "none";
	getbyId('button_disapproved').style.display = "none";
	getbyId('button_submit_propose').style.display = "block";
	getbyId('button_back').style.display = "block";
	getbyId('button_edit').style.display = "none"
	getbyId('button_update_committee').style.display = "none";
}

function show_recom(){
	getbyId('sel_committee_propose').style.display = "none";
	getbyId('button_reffer').style.display = "block";
	getbyId('button_disapproved').style.display = "block";
	getbyId('button_submit_propose').style.display = "none";
	getbyId('button_back').style.display = "none";
	getbyId('button_edit').style.display = "none"
	getbyId('button_update_committee').style.display = "none";
}


function back(){
	getbyId('sel_committee_propose').style.display = "none";
	getbyId('button_reffer').style.display = "block";
	getbyId('button_disapproved').style.display = "block";
	getbyId('button_submit_propose').style.display = "none";
	getbyId('button_back').style.display = "none";
	getbyId('button_edit').style.display = "none"
	getbyId('button_update_committee').style.display = "none";
}

function show_edit(){
	getbyId('sel_committee_propose').style.display = "none";
	getbyId('button_reffer').style.display = "none";
	getbyId('button_disapproved').style.display = "none";
	getbyId('button_submit_propose').style.display = "none";
	getbyId('button_back').style.display = "none";
	getbyId('button_update_committee').style.display = "none";

	getbyId('button_edit').style.display = "block"
}

function show_edit2()
{
	getbyId('sel_committee_propose2').style.display = "none";
	getbyId('button_reffer2').style.display = "none";
	getbyId('button_disapproved2').style.display = "none";
	getbyId('button_submit_propose2').style.display = "none";
	getbyId('button_back2').style.display = "none";
	getbyId('button_update_committee2').style.display = "none";

	getbyId('button_edit2').style.display = "block"
}

function show_com2(){
	getbyId('sel_committee_propose2').style.display = "block";
	getbyId('button_reffer2').style.display = "none";
	getbyId('button_disapproved2').style.display = "none";
	getbyId('button_submit_propose2').style.display = "block";
	getbyId('button_back2').style.display = "block";
	getbyId('button_edit2').style.display = "none"
	getbyId('button_update_committee2').style.display = "none";
}

function show_recom2(){
	getbyId('sel_committee_propose2').style.display = "none";
	getbyId('button_reffer2').style.display = "block";
	getbyId('button_disapproved2').style.display = "block";
	getbyId('button_submit_propose2').style.display = "none";
	getbyId('button_back2').style.display = "none";
	getbyId('button_edit').style.display = "none"
	getbyId('button_update_committee2').style.display = "none";
}

function back2(){
	getbyId('sel_committee_propose2').style.display = "none";
	getbyId('button_reffer2').style.display = "block";
	getbyId('button_disapproved2').style.display = "block";
	getbyId('button_submit_propose2').style.display = "none";
	getbyId('button_back2').style.display = "none";
	getbyId('button_edit2').style.display = "none"
	getbyId('button_update_committee2').style.display = "none";
}

function edit_propose2(){
	getbyId('sel_committee_propose2').style.display = "none";
	getbyId('button_reffer2').style.display = "none";
	getbyId('button_disapproved2').style.display = "none";
	getbyId('button_submit_propose2').style.display = "none";
	getbyId('button_back2').style.display = "none";

	getbyId('button_edit2').style.display = "none"

	getbyId('button_update_committee2').style.display = "block";
	getbyId('sel_committee_propose2').style.display = "block";
	getbyId('button_disapproved2').style.display = "block";
}

function edit_propose(){
	getbyId('sel_committee_propose').style.display = "none";
	getbyId('button_reffer').style.display = "none";
	getbyId('button_disapproved').style.display = "none";
	getbyId('button_submit_propose').style.display = "none";
	getbyId('button_back').style.display = "none";

	getbyId('button_edit').style.display = "none"

	getbyId('button_update_committee').style.display = "block";
	getbyId('sel_committee_propose').style.display = "block";
	getbyId('button_disapproved').style.display = "block";
}

function show_document_downloadable(data){
	getbyId('ul_documents_downloadable').innerHTML = "";
	var ul = getbyId('ul_documents_downloadable');
	for(var x=0; x<data.length;x++){
		var li = document.createElement('li')
		li.className="list-group-item d-flex"
		var p = document.createElement("p")
		p.className="p-0 m-0 flex-grow-1"
		p.style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;"
		let split= data[x].split("\\")
		p.innerHTML = split[split.length - 1]
		var a = document.createElement("a")
		a.className="btn btn-default"
		a.innerHTML ="Download"
		a.href= "/static/uploads/" + data[x]
		a.target = "_blank"

		li.appendChild(p)
		li.appendChild(a)
		ul.appendChild(li)
	}

	$("#show_document_modal").modal('show');
}