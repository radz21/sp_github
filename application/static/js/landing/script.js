function onGetFile(el) {
 var file = el. files[0]

 var options = { inWrapper: false, ignoreWidth: true, ignoreHeight: true }

 docx.renderAsync(file, document.getElementById("open_docs"), null, options)
   .then(x => console.log("docx: finished"));
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


function PreviewWordDoc(inp_id) {
    //Read the Word Document data from the File Upload.
    var doc = document.getElementById(inp_id).files[0];

    //If Document not NULL, render it.
    if (doc != null) {
        //Set the Document options.
        var docxOptions = Object.assign(docx.defaultOptions, {
            useMathMLPolyfill: true
        });

        //Reference the Container DIV.
        var container = document.querySelector("#open_docs");

        //Render the Word Document.
        docx.renderAsync(doc, container, null, docxOptions);
    }
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
