function getCommitteeBysp(id, sel){
	var data ={
		sp_id: id
	}
	
	sendDataWithCallback('/get_committeeBySp', data ,function(res) {
        $('#'+ sel).chosen({width:"100%"})
        
        if(sel=='list_committee_reports'){
        	$('#' + sel).append(`<option value="" disabled selected>--SELECT--</option>`);
        }
		for(var x=0; x<res.length; x++){
			$('#' + sel).append(`<option value="${res[x].committee_id}"> ${res[x].committee} </option>`);
		}

		$('#' + sel).trigger("chosen:updated")
    })
}

function getCommittee_by_sp(elem,id){
    sendDataWithCallback('/get_committeeBySp',{sp_id:id},function(res){
        if(res){
            getbyId(elem).innerHTML = ""
            $('#' + elem).append(`<option value="" disabled selected> ${'--SELECT--'} </option>`);
            for(var x=0; x<res.length; x++){
                $('#' + elem).append(`<option value="${res[x].committee_id}"> ${res[x].committee} </option>`);
            }

            $('#' + elem).trigger("chosen:updated")
        }
    })
}