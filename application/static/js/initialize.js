let committeeBySp = []
let getLogo = []
let count_documents=[]
let get_city_name=[]
let get_sp_active=[]
let get_all_active_councilor=[]
let get_committee=[]
let get_document_tracking_not_approved = []
let get_minutes = []
let get_personal_info=[]
let get_source_document=[]

function fetchDataForm(url,data) {
    return new Promise((resolve, reject) => {
        sendDataWithCallback(url,data,function(res){
            if (res) {
                resolve(res);
            } else {
                reject(`Failed to fetch data from ${url}`);
            }
        })
    });
}

function fetchData(url) {
    return new Promise((resolve, reject) => {
        getDataWithCallback(url, function(res) {
            if (res) {
                resolve(res);
            } else {
                reject(`Failed to fetch data from ${url}`);
            }
        });
    });
}

async function initializeData() {
    try {
        // committeeBySp = await fetchData('/get_committeeBySp');
        getLogo = await fetchData('/get_logo');
        count_documents = await fetchData('/count_documents');
        get_city_name = await fetchData('/get_city_name');
        get_sp_active = await fetchData('/get_sp_active')
        get_all_active_councilor = await fetchData('/get_all_active_councilor')
        get_committee = await fetchData('/get_committee')
        get_document_tracking_not_approved = await fetchData('/get_document_tracking_not_approved')
        get_minutes = await fetchData('/get_minutes')
        get_personal_info = await fetchData('/sel_personal_info')
        get_source_document = await fetchData('/get_source_document')
        return true

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
