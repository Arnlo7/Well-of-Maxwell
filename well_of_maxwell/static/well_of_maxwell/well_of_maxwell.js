
"use strict"

/* Helper Functions used for all pages:*/
function displayError(message){
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

function deleteModule(id){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateEditPage(xhr)
    }
    xhr.open("POST", "/well_of_maxwelldelete-module", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("module_id="+id+"&csrfmiddlewaretoken="+getCSRFToken());
    location.reload()
}

function addContent(id){
    let content_find = "id_content_input_text_"+id
    let itemTextElement = document.getElementById(content_find)
    let itemTextValue = itemTextElement.value
    itemTextElement.value = ""
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateEditPage(xhr)
    }
    xhr.open("POST", "/well_of_maxwelladd-content", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("module_id="+id+"&section_title="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addText(id){
    let text_find = "id_text_input_text_"+id
    let itemTextElement = document.getElementById(text_find)
    let itemTextValue = itemTextElement.value
    itemTextElement.value = ""
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateEditPage(xhr)
    }
    xhr.open("POST", "/well_of_maxwelladd-text", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("content_id="+id+"&text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addImage(id){
    let image_find = "id_image_input_image_"+id
    let itemTextElement = document.getElementById(image_find)
    let itemTextValue = itemTextElement.value
    itemTextElement.value = ""
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateEditPage(xhr)
    }
    
    xhr.open("POST", "/well_of_maxwelladd-image", true);
    xhr.setRequestHeader("Content-type", `multipart/form-data,boundary=${boundary}`);
    xhr.sendAsBinary("content_id="+id+"&image="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

/*Functions for updating the Edit Home Page */
function updateEditPage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateEditHome(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateEditHome(item_dict) {
    let moduleList = document.getElementById("my-modules-go-here")
    let items = item_dict['modules']
    for (let i = 0; i< items.length; i++){
        let curr_module = items[i]
        let element = document.createElement("div")
        let check = document.getElementById("id_module_div_" + curr_module.id)
        if (check == null && curr_module.module_type == 0){
        element.innerHTML = '<div class ="row" id="id_module_div_' + curr_module.id + '">' +
                            '<div>'+
                            'Module ' + curr_module.number + ":" +
                            '<button class= "btn btn-danger" id="id_delete_button'+curr_module.id+'"'+'onclick="deleteModule('+curr_module.id+')">Delete Module</button>'+
                            '</div>' +
                            '<div class = "card shadow p-3 mb-5 bg-white rounded">' + 
                            'Module Title:' + curr_module.page_title + 
                            '<div> Module Image:' + curr_module.page_image + 
                            '<div id= "my-content-go-here-for-module-'+curr_module.id+'">'+
                            '</div>' +
                            '<label>Add Content: </label>'+
                            '<input class="form-control form-control-lg" type = "text" id = "id_content_input_text_'+curr_module.id+'"'+' name ="comment"></input>'+
                            '<button  class= "btn btn-success" id="id_content_button'+curr_module.id+'"'+'onclick="addContent('+curr_module.id+')">Submit</button>'+
                            '</div>' + 
                            '</div>'
        moduleList.insertBefore(element,moduleList.firstChild)
        }
        let contentList = document.getElementById("my-content-go-here-for-module-"+curr_module.id)
        let content = item_dict['content']
        for (let j = 0; j < content.length; j++){
            let curr_content = content[j]
            let element = document.createElement("div")
            let check = document.getElementById("id_content_div_"+curr_content.id)
            if (check == null && curr_module.module_type == 0 && curr_content.module_id == curr_module.id ){
            element.innerHTML = '<div class = "indent" id="id_content_div_'+curr_content.id +'">' +
                                'Section Title:' + curr_content.section_title +
                                '<div id= "my-text-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                '<label>Add Text: </label>'+
                                '<input class="form-control form-control-lg" type = "text" id = "id_text_input_text_'+curr_content.id+'"'+' name ="text"></input>'+
                                '<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+'onclick="addText('+curr_content.id+')">Submit</button>'+
                                '<div id= "my-image-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                //'<label>Add Image: </label>'+
                                //'<input class="form-control form-control-lg" type = "file" id = "id_image_input_image_'+curr_content.id+'"'+' name ="image"></input>'+
                                //'<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+' type="submit">Submit</button>'+ 
                                '</div>'+
                                '</div>'
            contentList.insertBefore(element,contentList.firstChild)
            }

            let textList = document.getElementById("my-text-go-here-for-content-"+curr_content.id)
            if(textList == null){
                continue
            }
            let text = item_dict['text']
            for (let k = 0; k <text.length; k++){
                let curr_text = text[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_text.id)
                if (check == null && curr_module.module_type == 0 && curr_text.module_id == curr_module.id && curr_text.content_id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_text.id + '">' +
                                    'Text:' + curr_text.text +
                                    '</div>'
                
                textList.insertBefore(element,textList.firstChild)
                }
            }
            let imageList = document.getElementById("my-image-go-here-for-content-"+curr_content.id)
            if(imageList == null){
                continue
            }
            let image = item_dict['image']
            for (let k = 0; k <image.length; k++){
                let curr_image = image[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_image.id)
                if (check == null && curr_module.module_type == 0 && curr_image.module_id == curr_module.id && curr_image.content_id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_image.id + '">' +
                                    'Image Name:' + curr_image.image +
                                    '</div>'
                
                imageList.insertBefore(element,imageList.firstChild)
                }
            }
        }
    }
}

function loadEditHome(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateEditPage(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellget-edit-modules", true)
    xhr.send()
}

/*Functions for updating the Experiment 1 Page */
function updateEditExperiment_1Page(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateEditExperiment_1Home(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateEditExperiment_1Home(item_dict) {
    let moduleList = document.getElementById("my-modules-go-here")
    let items = item_dict['modules']
    for (let i = 0; i< items.length; i++){
        let curr_module = items[i]
        let element = document.createElement("div")
        let check = document.getElementById("id_module_div_" + curr_module.id)
        if (check == null && curr_module.module_type == 1){
        element.innerHTML = '<div class ="row" id="id_module_div_' + curr_module.id + '">' +
                            '<div>'+
                            'Module ' + curr_module.number + ":" +
                            '<button class= "btn btn-danger" id="id_delete_button'+curr_module.id+'"'+'onclick="deleteModule('+curr_module.id+')">Delete Module</button>'+
                            '</div>' +
                            '<div class = "card shadow p-3 mb-5 bg-white rounded">' + 
                            'Module Title:' + curr_module.page_title + 
                            '<div> Module Image:' + curr_module.page_image + 
                            '<div id= "my-content-go-here-for-module-'+curr_module.id+'">'+
                            '</div>' +
                            '<label>Add Content: </label>'+
                            '<input class="form-control form-control-lg" type = "text" id = "id_content_input_text_'+curr_module.id+'"'+' name ="comment"></input>'+
                            '<button  class= "btn btn-success" id="id_content_button'+curr_module.id+'"'+'onclick="addContent('+curr_module.id+')">Submit</button>'+
                            '</div>' + 
                            '</div>'
        moduleList.insertBefore(element,moduleList.firstChild)
        }
        let contentList = document.getElementById("my-content-go-here-for-module-"+curr_module.id)
        let content = item_dict['content']
        for (let j = 0; j < content.length; j++){
            let curr_content = content[j]
            let element = document.createElement("div")
            let check = document.getElementById("id_content_div_"+curr_content.id)
            if (check == null && curr_module.module_type == 1 && curr_content.module_id == curr_module.id){
            element.innerHTML = '<div class = "indent" id="id_content_div_'+curr_content.id +'">' +
                                'Section Title:' + curr_content.section_title +
                                '<div id= "my-text-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                '<label>Add Text: </label>'+
                                '<input class="form-control form-control-lg" type = "text" id = "id_text_input_text_'+curr_content.id+'"'+' name ="text"></input>'+
                                '<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+'onclick="addText('+curr_content.id+')">Submit</button>'+
                                '<div id= "my-image-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                //'<label>Add Image: </label>'+
                                //'<input class="form-control form-control-lg" type = "file" id = "id_image_input_image_'+curr_content.id+'"'+' name ="image"></input>'+
                                //'<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+' type="submit">Submit</button>'+ 
                                '</div>'+
                                '</div>'
            contentList.insertBefore(element,contentList.firstChild)
            }

            let textList = document.getElementById("my-text-go-here-for-content-"+curr_content.id)
            if(textList == null){
                continue
            }
            let text = item_dict['text']
            for (let k = 0; k <text.length; k++){
                let curr_text = text[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_text.id)
                if (check == null && curr_module.module_type == 1 && curr_text.module_id == curr_module.id && curr_text.content_id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_text.id + '">' +
                                    'Text:' + curr_text.text +
                                    '</div>'
                
                textList.insertBefore(element,textList.firstChild)
                }
            }
            let imageList = document.getElementById("my-image-go-here-for-content-"+curr_content.id)
            if(imageList == null){
                continue
            }
            let image = item_dict['image']
            for (let k = 0; k <image.length; k++){
                let curr_image = image[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_image.id)
                if (check == null && curr_module.module_type == 1 && curr_image.content.module_id == curr_module.id && curr_image.content.id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_image.id + '">' +
                                    'Image Name:' + curr_image.image +
                                    '</div>'
                
                imageList.insertBefore(element,imageList.firstChild)
                }
            }
        }
    }
}

function loadEditExperiment_1(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateEditExperiment_1Page(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellget-edit-modules", true)
    xhr.send()
}

/* Integration */
/* Read from csv file with current voltages*/
function checkVoltageExp1(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateVoltageExp1Page(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellget-voltage-exp1", true)
    xhr.send()
}

function updateVoltageExp1Page(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateVoltageExp1Home(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateVoltageExp1Home(item_dict) {
    let voltageList = document.getElementById("my-voltage-go-here")
    /*
    let check = document.getElementById("id_header_div")
    if(check == null){
        let element = document.createElement("div")
        element.innerHTMl = '<div id = "id_header_div">'
                            'Highest:' + item_dict['highest'] +
                            'Lowest:' + item_dict['lowest'] +
                            'Peak to Peak:' + item_dict['pp'] +
                            '</div>'
        voltageList.insertBefore(element,voltageList.firstChild)
    }  
    */
    /*let items = item_dict['voltage']*/
    /*"<img src='http://localhost/well_of_maxwell/images/plot.png' width = 200px></img>"*/
    /*for (let i = 0; i< items.length; i++){*/
    for (let i = 0; i< 1; i++){
        /*let curr_voltage = items[i]*/
        let element = document.createElement("div")
        let check = document.getElementById("id_voltage_div_" + i)
        let temp = voltageList.firstChild
        if (check==null){
            element.innerHTML = `<img id="id_voltage_div_` + i + `"src='/well_of_maxwellget-plot/${item_dict['photo_id']}'></img>`
            voltageList.appendChild(element,voltageList.firstChild)
        }
        else{
            element.innerHTML = `<img id="id_voltage_div_` + i + `"src='/well_of_maxwellget-plot/${item_dict['photo_id']}'></img>`
            voltageList.removeChild(temp)
            voltageList.appendChild(element,voltageList.firstChild)
        }
        /*
        if (check==null){
            element.innerHTML = '<div class ="row" id="id_voltage_div_' + i + '">' +
                            'Voltage ' + i + ":" + items[i]
                            '</div>'
            voltageList.appendChild(element,voltageList.firstChild)
        }
        else{
            check.innerHTML = '<div class ="row" id="id_voltage_div_' + i + '">' +
                                'Voltage ' + i + ":" + items[i]
                                '</div>'   
        }
        */
    }
}

/*Update csv file with new voltages */
function checkVoltageUpdateExp1(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateVoltageExp1UpdatePage(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellread-voltage-exp1", true)
    xhr.send()
}

function updateVoltageExp1UpdatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateVoltageExp1UpdateHome(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateVoltageExp1UpdateHome(item_dict) {
    console.log("hi")
}

/*Functions for updating the Experiment 2 Page */
function updateEditExperiment_2Page(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateEditExperiment_2Home(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateEditExperiment_2Home(item_dict) {
    let moduleList = document.getElementById("my-modules-go-here")
    let items = item_dict['modules']
    for (let i = 0; i< items.length; i++){
        let curr_module = items[i]
        let element = document.createElement("div")
        let check = document.getElementById("id_module_div_" + curr_module.id)
        if (check == null && curr_module.module_type == 2){
        element.innerHTML = '<div class ="row" id="id_module_div_' + curr_module.id + '">' +
                            '<div>'+
                            'Module ' + curr_module.number + ":" +
                            '<button class= "btn btn-danger" id="id_delete_button'+curr_module.id+'"'+'onclick="deleteModule('+curr_module.id+')">Delete Module</button>'+
                            '</div>' +
                            '<div class = "card shadow p-3 mb-5 bg-white rounded">' + 
                            'Module Title:' + curr_module.page_title + 
                            '<div> Module Image:' + curr_module.page_image + 
                            '<div id= "my-content-go-here-for-module-'+curr_module.id+'">'+
                            '</div>' +
                            '<label>Add Content: </label>'+
                            '<input class="form-control form-control-lg" type = "text" id = "id_content_input_text_'+curr_module.id+'"'+' name ="comment"></input>'+
                            '<button  class= "btn btn-success" id="id_content_button'+curr_module.id+'"'+'onclick="addContent('+curr_module.id+')">Submit</button>'+
                            '</div>' + 
                            '</div>'
        moduleList.insertBefore(element,moduleList.firstChild)
        }
        let contentList = document.getElementById("my-content-go-here-for-module-"+curr_module.id)
        let content = item_dict['content']
        for (let j = 0; j < content.length; j++){
            let curr_content = content[j]
            let element = document.createElement("div")
            let check = document.getElementById("id_content_div_"+curr_content.id)
            if (check == null && curr_module.module_type == 2 && curr_content.module_id == curr_module.id){
            element.innerHTML = '<div class = "indent" id="id_content_div_'+curr_content.id +'">' +
                                'Section Title:' + curr_content.section_title +
                                '<div id= "my-text-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                '<label>Add Text: </label>'+
                                '<input class="form-control form-control-lg" type = "text" id = "id_text_input_text_'+curr_content.id+'"'+' name ="text"></input>'+
                                '<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+'onclick="addText('+curr_content.id+')">Submit</button>'+
                                '<div id= "my-image-go-here-for-content-'+curr_content.id+'">'+
                                '</div>' +
                                //'<label>Add Image: </label>'+
                                //'<input class="form-control form-control-lg" type = "file" id = "id_image_input_image_'+curr_content.id+'"'+' name ="image"></input>'+
                                //'<button class= "btn btn-success" id="id_text_button'+curr_content.id+'"'+' type="submit">Submit</button>'+ 
                                '</div>'+
                                '</div>'
            contentList.insertBefore(element,contentList.firstChild)
            }

            let textList = document.getElementById("my-text-go-here-for-content-"+curr_content.id)
            if(textList == null){
                continue
            }
            let text = item_dict['text']
            for (let k = 0; k <text.length; k++){
                let curr_text = text[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_text.id)
                if (check == null && curr_module.module_type == 2 && curr_text.module_id == curr_module.id && curr_text.content_id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_text.id + '">' +
                                    'Text:' + curr_text.text +d
                                    '</div>'
                
                textList.insertBefore(element,textList.firstChild)
                }
            }
            let imageList = document.getElementById("my-image-go-here-for-content-"+curr_content.id)
            if(imageList == null){
                continue
            }
            let image = item_dict['image']
            for (let k = 0; k <image.length; k++){
                let curr_image = image[k]
                let element = document.createElement("div")
                let check = document.getElementById("id_text_div_"+curr_image.id)
                if (check == null && curr_module.module_type == 2 && curr_image.content.module_id == curr_module.id && curr_image.content.id == curr_content.id){
                element.innerHTML = '<div class = "indent" id="id_text_div_'+curr_image.id + '">' +
                                    'Image Name:' + curr_image.image +
                                    '</div>'
                
                imageList.insertBefore(element,imageList.firstChild)
                }
            }
        }
    }
}

function loadEditExperiment_2(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateEditExperiment_2Page(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellget-edit-modules", true)
    xhr.send()
}

/* Integration */
/* Read from csv file with current voltages*/
function checkVoltageExp2(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateVoltageExp2Page(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellget-voltage-exp2", true)
    xhr.send()
}

function updateVoltageExp2Page(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateVoltageExp2Home(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateVoltageExp2Home(item_dict) {
    let voltageList = document.getElementById("my-voltage-go-here")
    /*
    let check = document.getElementById("id_header_div")
    if(check == null){
        let element = document.createElement("div")
        element.innerHTMl = '<div id = "id_header_div">'
                            'Highest:' + item_dict['highest'] +
                            'Lowest:' + item_dict['lowest'] +
                            'Peak to Peak:' + item_dict['pp'] +
                            '</div>'
        voltageList.insertBefore(element,voltageList.firstChild)
    }  
    */
    /*let items = item_dict['voltage']*/
    /*"<img src='http://localhost/well_of_maxwell/images/plot.png' width = 200px></img>"*/
    /*for (let i = 0; i< items.length; i++){*/
    for (let i = 0; i< 1; i++){
        /*let curr_voltage = items[i]*/
        let element = document.createElement("div")
        let check = document.getElementById("id_voltage_div_" + i)
        let temp = voltageList.firstChild
        if (check==null){
            element.innerHTML = `<img id="id_voltage_div_` + i + `"src='/well_of_maxwellget-plot/${item_dict['photo_id']}'></img>`
            voltageList.appendChild(element,voltageList.firstChild)
        }
        else{
            element.innerHTML = `<img id="id_voltage_div_` + i + `"src='/well_of_maxwellget-plot/${item_dict['photo_id']}'></img>`
            voltageList.removeChild(temp)
            voltageList.appendChild(element,voltageList.firstChild)
        }
        /*
        if (check==null){
            element.innerHTML = '<div class ="row" id="id_voltage_div_' + i + '">' +
                            'Voltage ' + i + ":" + items[i]
                            '</div>'
            voltageList.appendChild(element,voltageList.firstChild)
        }
        else{
            check.innerHTML = '<div class ="row" id="id_voltage_div_' + i + '">' +
                                'Voltage ' + i + ":" + items[i]
                                '</div>'   
        }
        */
    }
}

/*Update csv file with new voltages */
function checkVoltageUpdateExp2(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(xhr.readyState!=4) return updateVoltageExp2UpdatePage(xhr)  
    }
    xhr.open("GET", "/well_of_maxwellread-voltage-exp2", true)
    xhr.send()
}

function updateVoltageExp2UpdatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateVoltageExp2UpdateHome(response)
        return
    }
    if (xhr.status == 0){
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json'){
        displayError('Recieved status = ' + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if(response.hasOwnProperty('error')){
        displayError(response.error)
        return
    }
    displayError(response)
}

function updateVoltageExp2UpdateHome(item_dict) {
    console.log("hi")
}