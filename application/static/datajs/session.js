var document_tracking = [];

var persons = [];
var committee = [];

var link_list = [];
var minutes_list = [];

function get_session() {
    if ($.fn.DataTable.isDataTable("#tbl_session")) {
        $("#tbl_session").DataTable().destroy();
    }

    var table=$('#tbl_session').DataTable({
        responsive: true,
        searching: true,
        "ajax": {
            "type": "GET",
            "url": '/get_session',
            "dataSrc": function(data) {
                data.forEach(function(item){
                    var open_doc = `<button type='button' class="btn btn-sm btn-icon text-primary flex-end" data-bs-toggle="tooltip" title="Edit" onclick='open_session(this)'>
                    <span class="btn-inner">
                        <svg width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" >
                            <path d="M11.4925 2.78906H7.75349C4.67849 2.78906 2.75049 4.96606 2.75049 8.04806V16.3621C2.75049 19.4441 4.66949 21.6211 7.75349 21.6211H16.5775C19.6625 21.6211 21.5815 19.4441 21.5815 16.3621V12.3341" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M8.82812 10.921L16.3011 3.44799C17.2321 2.51799 18.7411 2.51799 19.6721 3.44799L20.8891 4.66499C21.8201 5.59599 21.8201 7.10599 20.8891 8.03599L13.3801 15.545C12.9731 15.952 12.4211 16.181 11.8451 16.181H8.09912L8.19312 12.401C8.20712 11.845 8.43412 11.315 8.82812 10.921Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                            <path d="M15.1655 4.60254L19.7315 9.16854" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>
                    </span>
                    </button>`

                    var live_session = `<button type='button' class="btn btn-sm btn-icon text-primary flex-end" data-bs-toggle="tooltip" title="Order of business" onclick='order_of_business(this)'>
                    <span class="btn-inner">
                        <svg class="svg-icon" viewBox="0 0 20 20">
                            <path d="M10,1.445c-4.726,0-8.555,3.829-8.555,8.555c0,4.725,3.829,8.555,8.555,8.555c4.725,0,8.555-3.83,8.555-8.555C18.555,5.274,14.725,1.445,10,1.445 M10,17.654c-4.221,0-7.654-3.434-7.654-7.654c0-4.221,3.433-7.654,7.654-7.654c4.222,0,7.654,3.433,7.654,7.654C17.654,14.221,14.222,17.654,10,17.654 M14.39,10c0,0.248-0.203,0.45-0.45,0.45H6.06c-0.248,0-0.45-0.203-0.45-0.45s0.203-0.45,0.45-0.45h7.879C14.187,9.55,14.39,9.752,14.39,10 M14.39,12.702c0,0.247-0.203,0.449-0.45,0.449H6.06c-0.248,0-0.45-0.202-0.45-0.449c0-0.248,0.203-0.451,0.45-0.451h7.879C14.187,12.251,14.39,12.454,14.39,12.702 M14.39,7.298c0,0.248-0.203,0.45-0.45,0.45H6.06c-0.248,0-0.45-0.203-0.45-0.45s0.203-0.45,0.45-0.45h7.879C14.187,6.848,14.39,7.051,14.39,7.298"></path>
                        </svg>
                    </span>
                    </button>`

                    item.btn = open_doc + live_session;
                });
                
                return data;
            }
        },
        dom: 'Bfrtip',
        columns: [
            { data: 'session_number' },
            { data: 'session_type' , render : (data, type, row)=>{
                return data + " SESSION"
            }},
            { data: 'session_date' },
            { data: 'sp_title' },
            { data: 'sp_year' },
            { data: 'btn'}
        ],
        buttons: [{
            text: "add",
            action: function(e, dt, node, config) {
                    clear_session_data(function(){
                    populate_active_councilor()
                    getbyId('btn_del_session').style.display = "none";
                    $("#div_session_add").modal("toggle");

                });
            },
            'className': 'btn btn-sm btn-primary'
        },{
            extend: 'print',
            text: 'Print',
            filename: 'file',
            title: 'Print',
            titleAttr: 'Print'
            ,'className': 'btn btn-sm btn-warning'
        },

        {
            text: 'Filter Session Type',
            className: 'dt-filter-select',  // custom class for styling
            action: function () {},
            init: function(api, node, config) {
                $(node).empty().append(`
                    <select id="filter_session_type" class="form-select form-select-sm" style="width: 180px;">
                        <option value="">All Session Types</option>
                        <option value="REGULAR">REGULAR SESSION</option>
                        <option value="SPECIAL">SPECIAL SESSION</option>
                        <option value="JOINT">JOINT SESSION</option>
                    </select>
                `);

                // Bind filtering logic to change event
                $(node).find('select').on('change', function () {
                    const val = this.value;
                    api.column(1).search(val ? '^' + val + ' SESSION$' : '', true, false).draw();
                });
            }
        }

        ],
        "pagingType": "full_numbers",
        "pageLength": 5,
         bStateSave:true,
         "ordering": false
    });
}

function delete_session() {
    swal.fire({
        title: "Are you sure want to delete this session?",
        text: "Click ok to continue",
        type: "info",
        showCancelButton: true,
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return fetch(console.log("log"))
            .then(
                $.ajax({
                    type: 'POST',
                    url: "/delete_session",
                    contentType:false,
                    processData:false,
                    cache: false,
                    data:JSON.stringify({"session_id": session_id}),
                    beforeSend: function() {
                       show_spinner2()
                    },
                    success: function(res) {
                        hide_spinner2()
                        $('#tbl_session').DataTable().ajax.reload();
                        clear_session_data(function(){
                            $("#div_session_add").modal('hide');
                        })

                        saved(res)
                    },
                    error: function() {
                        error_in_saving("error occured");
                    }
                })
            )
            .catch(() => {
                Swal.fire({
                  icon: 'error',
                  title: 'Error occured'
                })
            })
        }
    })
}

function clear_session_data(callback){
    byId("form_session").reset();

    byId("div_rollcall").innerHTML = "";
    rollCall = 0
    
    byId("div_reading_consideration").innerHTML = "";
    readingCount = 0

    byId("div_question_hour").innerHTML = "";
    questionCount = 0;

    byId("div_privilege_hour").innerHTML = "";
    privilege_hourCount = 0;

    byId("div_propose_ord").innerHTML = "";
    propose_ordCount = 0

    byId("div_propose_reso").innerHTML = "";
    propose_resoCount = 0

    byId("div_petitions_for_refferals").innerHTML = "";
    petitions_for_refferalsCount = 0

    byId("div_additional_refferals").innerHTML = "";
    additional_refferalsCount = 0

    byId("div_veto_message").innerHTML = "";
    veto_messageCount = 0

    byId("div_unfinished").innerHTML = "";
    unfinishedCount = 0

    byId("div_business1").innerHTML = "";
    bussiness1Count = 0

    byId("div_just_inserted").innerHTML = "";
    just_insertedCount = 0

    byId('calendar_measure').innerHTML = "";
    calendar_measureCount = 0;
    
    byId('new_measure').innerHTML = "";
    new_measureCount = 0;

    byId('div_bussiness_third').innerHTML = "";
    bussiness1Count = 0;

    byId('summary_correction').innerHTML = "";
    summaryCount = 0;

    byId('div_announcement_').innerHTML = "";
    announcement_Count = 0;

    byId('div_committee_report_').innerHTML = "";
    committee_reportCount = 0;

    byId('div_committee_information_').innerHTML = "";
    committee_informationCount = 0;

    rand_id = Math.floor(Math.random() * 9999999);
    callback(true)
}

let rollCall = 0;
function populateRollcall() {
  const parent = document.getElementById("div_rollcall");

  // Create container div for one roll call entry
  const container = document.createElement('div');
  container.id = `child${rollCall}`;
  container.style.marginTop = '1%';
  container.style.marginLeft = '20%';
  container.style.display = 'flex';
  container.style.gap = '1%'; // spacing between inputs and button

  // Create input element for name
  const input = document.createElement('input');
  input.name = `attendance[${rollCall}][names]`;
  input.placeholder = "Choose name";
  input.className = "form-control";
  input.style.width = '40%';
  input.setAttribute('list', 'councilor_list');
  input.required = true;

  input.onblur = function() {
    const list = document.getElementById('councilor_list');
    const isValid = Array.from(list.options).some(opt => opt.value === this.value);
    if (!isValid) {
      warning('Please select proper name');
      this.value = "";
    }
  };

  // Create select dropdown for attendance status
  const select = document.createElement('select');
  select.name = `attendance[${rollCall}][status]`;
  select.className = "form-control";
  select.style.width = '40%';

  const options = [
    { value: "0", text: "PRESENT" },
    { value: "1", text: "ABSENT" },
    { value: "2", text: "LEAVE" },
    { value: "3", text: "TRAVEL" },
    { value: "4", text: "PRESIDING OFFICER" }
  ];

  options.forEach(opt => {
    const optionEl = document.createElement('option');
    optionEl.value = opt.value;
    optionEl.textContent = opt.text;
    select.appendChild(optionEl);
  });

  // Create remove button
  const btn = document.createElement('button');
  btn.type = "button";
  btn.textContent = "x";
  btn.className = "btn btn-sm btn-danger";
  btn.style.marginLeft = '1%';
  btn.dataset.inpId = container.id;

  btn.onclick = function() {
    const id = this.dataset.inpId;
    const el = document.getElementById(id);
    if (el) el.remove();
  };

  // Append all elements to container
  container.appendChild(input);
  container.appendChild(select);
  container.appendChild(btn);

  // Insert new rollcall at the top
  parent.insertBefore(container, parent.firstChild);

  rollCall++;
}

// var rollCall = 0;
// function populateRollcall(){
//     var parent = byId("div_rollcall");

//     var child = createElem('div'),
//         inp = createElem('input'),
//         sel = createElem('select'),
//         opt1 = createElem('option'),
//         opt2 = createElem('option'),
//         opt3 = createElem('option'),
//         opt4 = createElem('option'),
//         opt5 = createElem('option'),
//         btn = createElem('button');


//         opt1.innerHTML = "PRESENT";
//         opt2.innerHTML = "ABSENT";
//         opt3.innerHTML = "LEAVE";
//         opt4.innerHTML = "TRAVEL";
//         opt5.innerHTML = "PRESIDING OFFICER";
//         opt1.value = "0";
//         opt2.value = "1";
//         opt3.value = "2";
//         opt4.value = "3";
//         opt5.value = "4";

//         child.style = "margin-top: 1%;margin-left:20%;";
//         child.id = "child"+rollCall;
//         inp.name = "rollCall"+rollCall+"[name]";
//         inp.setAttribute("placeholder","Choose name")
//         inp.className = "form-control";
//         inp.style = "width: 40%;float: left;";
//         inp.name = "attendance["+rollCall+"][names]"
//         inp.setAttribute('list','councilor_list');
//         inp.setAttribute('required','true');
//         inp.onblur = function() {
//             var list = document.getElementById('councilor_list')
//             flag = 0;
//             for(x = 0; x < list.options.length; x++) {
//                 if(this.value == list.options[x].value) {
//                     flag = 1
//                 }
//             }
//             if(flag == 0){
//                 warning('Please select proper name')
//                 this.value = ""
//             }
//         }

//         sel.style = "width: 40%;float: left;";
//         sel.className = "form-control";
//         sel.name = "attendance["+rollCall+"][status]";

//         btn.type = "button";
//         btn.style = "margin-left: 1%";
//         btn.innerHTML = "x";
//         btn.setAttribute('data-inp_id','child'+rollCall);
//         btn.className = "btn btn-sm btn-danger"
//         btn.onclick = function(){
//             var id = this.getAttribute('data-inp_id')
//             byId(id).remove();
//         }

//         sel.appendChild(opt1)
//         sel.appendChild(opt2)
//         sel.appendChild(opt3)
//         sel.appendChild(opt4)
//         sel.appendChild(opt5)

//         child.appendChild(inp);
//         child.appendChild(sel);
//         child.appendChild(btn);
//         parent.insertBefore(child,parent.firstChild);
//         rollCall++;
// }


var readingCount = 0;
function add_reading_consid(){
    var parent = getbyId('div_reading_consideration')
    var div = document.createElement('div')
    div.id = "reading_consid_prev_min"+ readingCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "MINUTES"

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='reading_consid_minutes_id' + readingCount;
    sel.id= sel_id
    sel.name="reading_consid_prev_min["+readingCount+"][minutes_id]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true
    sel.appendChild(option_blank);

    minutes_list.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['minutes_id'];
        option.innerHTML = `${i['title']} Dated: ${i['date']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','reading_consid_prev_min'+ readingCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)

    $(sel).chosen({width: "90%"})
    readingCount++;
}

var questionCount = 0;
function add_question_hour(){
    var parent = getbyId('div_question_hour')

    var div = document.createElement('div')
    div.id = "question_hour"+ questionCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px;  padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','question_hour'+questionCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "FULLNAME"

    var inp = document.createElement('input')
    inp.className = "form-control"
    inp.name="question_hour["+questionCount+"][fullname]";

    var label2 = document.createElement('label')
    label2.innerHTML = "Office"

    var inp2 = document.createElement('input')
    inp2.type = 'text';
    inp2.name="question_hour["+questionCount+"][office]";
    inp2.className = "form-control"

    var label3 = document.createElement('label')
    label3.innerHTML = "Designation"

    var inp3 = document.createElement('input')
    inp3.type = 'text';
    inp3.name="question_hour["+questionCount+"][designation]";
    inp3.className = "form-control"

    var label4 = document.createElement('label')
    label4.innerHTML = "Subject"

    var inp4 = document.createElement('textarea')
    inp4.type = 'text';
    inp4.className = "form-control"
    inp4.name="question_hour["+questionCount+"][subject]";

    var label5 = document.createElement('label')
    label5.innerHTML = "Import Your File"

    var inp5 = document.createElement('input')
    inp5.type = 'file';
    inp5.className = "form-control"
    inp5.name="question_hour["+questionCount+"][file]";
    inp5.id = "question_hour_file"+ questionCount;

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(inp)
    div2.appendChild(label2)
    div2.appendChild(inp2)
    div2.appendChild(label3)
    div2.appendChild(inp3)
    div2.appendChild(label4)
    div2.appendChild(inp4)
    div2.appendChild(label5)
    div2.appendChild(inp5)

    div.appendChild(div2)

    parent.insertBefore(div,parent.firstChild);
    questionCount++
}

var privilege_hourCount = 0;
function add_privilege_hour(){
    var parent = getbyId('div_privilege_hour')

    var div = document.createElement('div')
    div.id = "privilege_hour"+ privilege_hourCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','privilege_hour'+privilege_hourCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "NAME OF COUNCILOR"

    var sel = document.createElement('select')
    sel.className = "form-control"
    sel.name="privilege_hour["+privilege_hourCount+"][info_id]";
    var sel_id='privilege_hour_tracking_no' + privilege_hourCount;
    sel.id= sel_id

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    persons.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['info_id'];
        option.innerHTML = `${i['fullname']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "Import Your File"

    var inp2 = document.createElement('input')
    inp2.type = 'file';
    inp2.className = "form-control"
    inp2.multiple = ''
    inp2.name="privilege_hour["+ privilege_hourCount +"][file]";
    inp2.id = "privilege_hour_file"+ privilege_hourCount;

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(inp2)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    privilege_hourCount++;
}

var propose_ordCount = 0
function add_propose_ord(){
    var parent = getbyId('div_propose_ord')
    var div = document.createElement('div')
    div.id = "propose_ord"+ propose_ordCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='propose_ord_tracking_no' + propose_ordCount;
    sel.id= sel_id
    sel.name="propose_ord["+propose_ordCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true
    sel.appendChild(option_blank);

    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','propose_ord'+propose_ordCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)

    $(sel).chosen({width: "90%"})
    propose_ordCount++;
}

var propose_resoCount = 0
function add_propose_reso(){
    var parent = getbyId('div_propose_reso')
    var div = document.createElement('div')
    div.id = "propose_reso"+ propose_resoCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='propose_res_tracking_no' + propose_resoCount;
    sel.id= sel_id
    sel.name="propose_reso["+propose_resoCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true
    sel.appendChild(option_blank);

    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','propose_reso'+propose_resoCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)
    parent.appendChild(div)

    $(sel).chosen({width: "90%"})
    propose_resoCount++;
}

var petitions_for_refferalsCount = 0
function add_petitions_for_refferals(){
    var parent = getbyId('div_petitions_for_refferals')

    var div = document.createElement('div')
    div.id = "petitions_for_refferals"+ petitions_for_refferalsCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','petitions_for_refferals'+petitions_for_refferalsCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.className = "form-control"
    sel.name="petitions_for_refferals["+petitions_for_refferalsCount+"][tracking_no]";
    var sel_id='petitions_for_refferals_tracking_no' + petitions_for_refferalsCount;
    sel.id= sel_id

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "TYPE"

    var sel2 = document.createElement('select')
    sel2.style ="width: 100%;float: left;"
    sel2.className = "form-control";
    sel2.name="petitions_for_refferals["+petitions_for_refferalsCount+"][type]";
    var option_blank2 = document.createElement("option");
    option_blank2.innerHTML = "--SELECT--"
    option_blank2.value = ""
    option_blank2.disabled = true
    option_blank2.selected = true
    sel2.appendChild(option_blank2);
    var option2 = document.createElement("option");
    option2.value = 1
    option2.innerHTML = `For Refferal`;
    sel2.appendChild(option2);
    var option2 = document.createElement("option");
    option2.value = 2
    option2.innerHTML = `For Information`;
    sel2.appendChild(option2);

    var div_committee = document.createElement('div')

    sel2.onchange= function(){
        if(this.value==1){
            var label3 = document.createElement('label')
            label3.innerHTML = "Committee";
            label3.style.float ="left"

            var sel_committee = document.createElement('select')
            sel_committee.className = "form-control"
            sel_committee.name="petitions_for_refferals["+(petitions_for_refferalsCount - 1)+"][committee_id][]";
            var sel_id='petitions_for_refferals_committee' + (petitions_for_refferalsCount - 1);
            sel_committee.id= sel_id
            sel_committee.multiple = true

            committee.forEach(function(i){
                var option = document.createElement("option");
                option.value = i['committee_id'];
                option.innerHTML = `${i['committee']}`;
                sel_committee.appendChild(option);
            })

            div_committee.appendChild(label3)
            div_committee.appendChild(sel_committee)
            
            $(sel_committee).chosen({width: "100%", height:"55px"})

        }else{
            div_committee.innerHTML =""
        }

        div2.appendChild(div_committee)
    }

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(sel2)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    petitions_for_refferalsCount++;
}

var additional_refferalsCount = 0;
function add_additional_refferals(){
    var parent = getbyId('div_additional_refferals')

    var div = document.createElement('div')
    div.id = "additional_refferals"+ additional_refferalsCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','additional_refferals'+ additional_refferalsCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.className = "form-control"
    sel.name="additional_refferals["+additional_refferalsCount+"][tracking_no]";
    var sel_id='additional_refferals_tracking_no' + additional_refferalsCount;
    sel.id= sel_id

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "TYPE"

    var sel2 = document.createElement('select')
    sel2.style ="width: 100%;float: left;"
    sel2.className = "form-control";
    sel2.name="additional_refferals["+additional_refferalsCount+"][type]";
    var option_blank2 = document.createElement("option");
    option_blank2.innerHTML = "--SELECT--"
    option_blank2.value = ""
    option_blank2.disabled = true
    option_blank2.selected = true
    sel2.appendChild(option_blank2);
    var option2 = document.createElement("option");
    option2.value = 1
    option2.innerHTML = `For Refferal`;
    sel2.appendChild(option2);
    var option2 = document.createElement("option");
    option2.value = 2
    option2.innerHTML = `For Information`;
    sel2.appendChild(option2);

    var div_committee = document.createElement('div')
    sel2.onchange= function(){
        if(this.value==1){
            var label3 = document.createElement('label')
            label3.innerHTML = "Committee";
            label3.style.float ="left"

            var sel_committee = document.createElement('select')
            sel_committee.className = "form-control"
            sel_committee.name="additional_refferals["+ (additional_refferalsCount - 1)+"][committee_id][]";
            var sel_id='additional_refferals_committee' + (additional_refferalsCount - 1);
            sel_committee.id= sel_id
            sel_committee.multiple="MULTIPLE"
            committee.forEach(function(i){
                var option = document.createElement("option");
                option.value = i['committee_id'];
                option.innerHTML = `${i['committee']}`;
                sel_committee.appendChild(option);
            })

            div_committee.appendChild(label3)
            div_committee.appendChild(sel_committee)
            
            $(sel_committee).chosen({width: "100%", height:"55px"})
        }else{
            div_committee.innerHTML =""
        }
    }

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(sel2)
    div2.appendChild(div_committee)
    

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    additional_refferalsCount++;
}

var veto_messageCount = 0;
function add_veto_message(){
    var parent = getbyId('div_veto_message')
    var div = document.createElement('div')
    div.id = "veto_message"+ veto_messageCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='veto_message_tracking_no' + veto_messageCount;
    sel.id= sel_id
    sel.name="veto_message["+veto_messageCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','veto_message'+veto_messageCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    veto_messageCount++;
}

var committee_reportCount = 0;
function add_committee_report_(){
    var parent = getbyId('div_committee_report_')

    var div = document.createElement('div')
    div.id = "committee_report"+ committee_reportCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','committee_report'+committee_reportCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label = document.createElement('label')
    label.innerHTML = "Committee Report No."

    var input = document.createElement("input")
    input.className = "form-control"
    input.name="committee_report["+committee_reportCount+"][committee_report_no]";

    var label1 = document.createElement('label')
    label1.innerHTML = "Committee"

    var sel = document.createElement('select')
    sel.className = "form-control"
    sel.name="committee_report["+committee_reportCount+"][committee_id]";
    var sel_id='committee_report_tracking_no' + committee_reportCount;
    sel.id= sel_id

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    committee.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['committee_id'];
        option.innerHTML = `${i['committee']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "Import Your File"

    var inp2 = document.createElement('input')
    inp2.type = 'file';
    inp2.className = "form-control"
    inp2.multiple = ''
    inp2.name="committee_report["+ committee_reportCount +"][file]";
    inp2.id = "committee_report_file"+ committee_reportCount;

    div2.appendChild(button)
    div2.appendChild(label)
    div2.appendChild(input)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(inp2)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    committee_reportCount++;
}

var committee_informationCount = 0;
function add_committee_information_(){
    var parent = getbyId('div_committee_information_')

    var div = document.createElement('div')
    div.id = "committee_information"+ committee_informationCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','committee_information'+committee_informationCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label = document.createElement('label')
    label.innerHTML = "Committee Report No."

    var input = document.createElement("input")
    input.className = "form-control"
    input.name="committee_information["+committee_informationCount+"][committee_information_no]";

    var label1 = document.createElement('label')
    label1.innerHTML = "Committee"

    var sel = document.createElement('select')
    sel.className = "form-control"
    sel.name="committee_information["+committee_informationCount+"][committee_id]";
    var sel_id='committee_information_tracking_no' + committee_informationCount;
    sel.id= sel_id

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    committee.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['committee_id'];
        option.innerHTML = `${i['committee']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "Import Your File"

    var inp2 = document.createElement('input')
    inp2.type = 'file';
    inp2.className = "form-control"
    inp2.multiple = ''
    inp2.name="committee_information["+ committee_informationCount +"][file]";
    inp2.id = "committee_information_file"+ committee_informationCount;

    div2.appendChild(button)
    div2.appendChild(label)
    div2.appendChild(input)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(inp2)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    committee_informationCount++;
}

var unfinishedCount = 0;
function add_unfinished(){
    var parent = getbyId('div_unfinished')
    var div = document.createElement('div')
    div.id = "unfinished_bussiness"+ unfinishedCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='unfinished_bussiness_tracking_no' + unfinishedCount;
    sel.id= sel_id
    sel.name="unfinished_bussiness["+unfinishedCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','unfinished_bussiness'+unfinishedCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    unfinishedCount++;
}

var bussiness1Count = 0;
function add_bussiness1(){
    var parent = getbyId('div_business1')
    var div = document.createElement('div')
    div.id = "bussiness_of_the_day"+ bussiness1Count;

    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='bussiness_of_the_day_tracking_no' + bussiness1Count;
    sel.id= sel_id
    sel.name="bussiness_of_the_day["+bussiness1Count+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','bussiness_of_the_day'+bussiness1Count);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)

    $(sel).chosen({width: "90%"})
    bussiness1Count++;
}

var urgentCount = 0;
function add_urgent(){
    var parent = getbyId('div_urgent')
    var div = document.createElement('div')
    div.id = "urgent"+ urgentCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto; "

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='urgent_tracking_no' + urgentCount;
    sel.id= sel_id
    sel.name="urgent["+urgentCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','urgent'+urgentCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    urgentCount++;
}

var just_insertedCount = 0;
function add_just_inserted(){
    var parent = getbyId('div_just_inserted')
    var div = document.createElement('div')
    div.id = "just_inserted"+ just_insertedCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto; "

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='just_inserted_tracking_no' + just_insertedCount;
    sel.id= sel_id
    sel.name="just_inserted["+just_insertedCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','just_inserted'+ just_insertedCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    just_insertedCount++;
}

var calendar_measureCount = 0;
function add_calendar_measure(){
    var parent = getbyId('calendar_measure')
    var div = document.createElement('div')
    div.id = "calendar_measure"+ calendar_measureCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto; "

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='calendar_measure_tracking_no' + calendar_measureCount;
    sel.id= sel_id
    sel.name="calendar_measure["+ calendar_measureCount +"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','calendar_measure'+ calendar_measureCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    calendar_measureCount++;
}

var new_measureCount = 0;
function add_new_measure(){
    var parent = getbyId('new_measure')
    var div = document.createElement('div')
    div.id = "new_measure"+ new_measureCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%; margin: auto; "

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='new_measure_tracking_no' + new_measureCount;
    sel.id= sel_id
    sel.name="new_measure["+ new_measureCount +"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','new_measure'+ new_measureCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    new_measureCount++;
}

var bussiness_thirdCount = 0;
function add_bussiness_third(){
    var parent = getbyId('div_bussiness_third')
    var div = document.createElement('div')
    div.id = "bussiness_third"+ bussiness_thirdCount;

    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin: auto;"

    var label1 = document.createElement('label')
    label1.style = "float: left;width:100%!important"
    label1.innerHTML = "TRACKING NO."

    var sel = document.createElement('select')
    sel.style ="width: 80%;float: left;"
    sel.className = "form-control"
    var sel_id='bussiness_third_tracking_no' + bussiness_thirdCount;
    sel.id= sel_id
    sel.name="bussiness_third["+bussiness_thirdCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);
    
    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var button = document.createElement('button')
    button.type="button"
    button.innerHTML="X"
    button.setAttribute("style", "margin-left: 1%; color: white!important")
    button.className = "btn btn-sm btn-danger"
    button.setAttribute('data-inp_id','unfinished'+bussiness_thirdCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }
    
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(button)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "90%"})
    bussiness_thirdCount++;
}

var summaryCount = 0;
function add_summary_correction(){
    var parent = getbyId('summary_correction')

    var div = document.createElement('div')
    div.id = "summary"+ summaryCount;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','summary'+summaryCount);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "TRACKING NO"

    var sel = document.createElement('select')
    sel.className = "form-control"
    var sel_id='summary_tracking_no' + summaryCount;
    sel.id= sel_id
    sel.name="summary["+summaryCount+"][tracking_no]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    document_tracking.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['track_gen_id'];
        option.innerHTML = `${i['tracking_no']} -- ${i['title']}`;
        sel.appendChild(option);
    })

    var label3 = document.createElement('label')
    label3.innerHTML = "OLD TITLE"

    var inp3 = document.createElement('textarea')
    inp3.className = "form-control"
    var input='summary_title' + summaryCount;
    inp3.id= input;
    inp3.name="summary["+summaryCount+"][old_title]";

    sel.onchange = function() {
        var val = "";
        if(this.options[this.selectedIndex].text){
            val = this.options[this.selectedIndex].text.split("--")[1]
        }
        
        document.getElementById(input).value = val;
    }

    var label2 = document.createElement('label')
    label2.innerHTML = "NEW TITLE"

    var inp2 = document.createElement('textarea')
    inp2.className = "form-control"
    inp2.name="summary["+summaryCount+"][new_title]";

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(sel)
    
    div2.appendChild(label3)
    div2.appendChild(inp3)

    div2.appendChild(label2)
    div2.appendChild(inp2)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    summaryCount++;
}

var announcement_Count = 0;
function add_announcement(){
    var parent = getbyId('div_announcement_')

    var div = document.createElement('div')
    div.id = "announcement_"+ announcement_Count;
    var div2 = document.createElement('div')
    div2.style = "width: 90%;margin-top:20px; padding: 30px; margin: auto; margin-top: 20px"

    var button = document.createElement('button')
    button.type="button"
    button.className = "btn-close"
    button.setAttribute("style", "float:right;position:relative;top: -20px!important; left:20px!important")
    button.setAttribute('data-inp_id','announcement_'+announcement_Count);
    button.onclick = function(){
        var id = this.getAttribute('data-inp_id')
        byId(id).remove();
    }

    var label1 = document.createElement('label')
    label1.innerHTML = "COUNCILOR"

    var sel = document.createElement('select')
    sel.className = "form-control"
    var sel_id='announcement_councilor' + announcement_Count;
    sel.id= sel_id
    sel.name="announcement_["+ announcement_Count +"][info_id]";

    var option_blank = document.createElement("option");
    option_blank.innerHTML = "--SELECT--"
    option_blank.value = ""
    option_blank.disabled = true
    option_blank.selected = true

    sel.appendChild(option_blank);

    persons.forEach(function(i){
        var option = document.createElement("option");
        option.value = i['info_id'];
        option.innerHTML = `${i['fullname']}`;
        sel.appendChild(option);
    })

    var label2 = document.createElement('label')
    label2.innerHTML = "ANNOUNCEMENT"

    var inp2 = document.createElement('textarea')
    inp2.className = "form-control"
    inp2.name="announcement_["+ announcement_Count +"][announcement]";

    var label3 = document.createElement('label')
    label3.innerHTML = "Import Your File"

    var inp3 = document.createElement('input')
    inp3.type = 'file';
    inp3.className = "form-control"
    inp3.multiple = ''
    inp3.name="announcement_["+ announcement_Count +"][file]";
    inp3.id = "announcement_file"+ announcement_Count;

    div2.appendChild(button)
    div2.appendChild(label1)
    div2.appendChild(sel)
    div2.appendChild(label2)
    div2.appendChild(inp2)
    div2.appendChild(label3)
    div2.appendChild(inp3)

    div.appendChild(div2)

    parent.appendChild(div)
    $(sel).chosen({width: "100%", height:"55px"})
    announcement_Count++;
}
