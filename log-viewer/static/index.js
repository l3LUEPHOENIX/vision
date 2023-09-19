function addSource(form) {
    // Add a Source textarea based on a provided drop down to select from.
    var newSource = JSON.parse(form.sources.value);
    var newSourceName = newSource.Name;
    var newSourcePath = newSource.Path;
    var newSourceId = newSource.id;

    if (newSource ==  "NONE") {
        return null
    } else  if (document.getElementById(`${newSourceId}`)){
        // If a text area exists for what was selected, do nothing.
        return null
    } else {
        var newBox = `
        <div id="${newSourceId}-container" class="grid-item">
            <div class="grid-item-header">
                <div class="grid-item-header-title">${newSourceName}:${newSourcePath}</div>
                <div class="grid-item-header-checkbox-container">
                    <label for="checkbox" class="grid-item-header-checkbox-label">Follow</label>
                    <input type="checkbox" class="grid-item-header-checkbox">
                </div>
                <div class="grid-item-header-button-container">
                    <button onClick="clearTextarea(this)" class="grid-item-header-button">Clear</button>
                    <button class="grid-item-header-button">Download</button>
                    <button onClick="removeSource(this)" class="grid-item-header-button">Remove</button>
                    <button onClick="toggleHide(this)" class="grid-item-header-button" style="display:block;">-</button>
                </div>
            </div>
            <textarea id="${newSourceId}" class="grid-item-body" cols="80" rows="50" readonly="true" wrap="true"></textarea>
        </div>
        `;
        document.getElementById("data-container").innerHTML += newBox;
    };
};

function removeSource(elem) {
    // Remove a textarea from the page.
    var sourceBox = elem.parentNode.parentNode.parentNode;
    sourceBox.remove();
};

function changeFontSize(size) {
    // Change the fontsize for all textareas in the document.
    var myTextAreas = document.getElementsByTagName("textarea")
    for (i = 0; i < myTextAreas.length; i++) {
        myTextAreas[i].style.fontSize = size;
    };
};

function clearTextarea(elm) {
    // Clear all text out of the given textarea.
    var myTextArea = elm.parentNode.parentNode.parentNode.getElementsByTagName("textarea");
    myTextArea[0].textContent = '';
};

function toggleHide(elm) {
    // When clicked, will toggle between showing text area and hiding it.
    var myTextArea = elm.parentNode.parentNode.parentNode.getElementsByTagName("textarea");
    if (myTextArea[0].style.display == "block") {
        myTextArea[0].style.display = "none";
        elm.textContent = "+";
    } else {
        myTextArea[0].style.display = "block";
        elm.textContent = "-";
    };
};

// The event streams
var source = new EventSource("/stream"); // {{ url_for('sse.stream') }}
source.addEventListener('event', function(event) {  
    var data = JSON.parse(event.data);
    // Add the newest entry into it's respective textarea, if there is currently a textarea for it.
    if (document.getElementById(`${data.source}`)) {
        document.getElementById(`${data.source}`).textContent += `${data.message}\n`;
    };
    
    // Check to see if each grid-item's follow checkbox is checked. If it is, auto-scroll
    // the text area to the bottom of the page. If this is checked while data is being added
    // to the textarea, and the user tries to scroll, their scrolling will be interupted.
    var myCheckBoxes = document.getElementsByClassName("grid-item-header-checkbox");
    var myTextAreas = document.getElementsByClassName("grid-item-body");
    for (i = 0; i < myCheckBoxes.length; i++) {
        if (myCheckBoxes[i].checked) {
            
            myTextAreas[i].scrollTop = myTextAreas[i].scrollHeight;
        
        };
    };

}, false);
source.addEventListener('error', function(event) {
    alert("Failed to connect to event stream. Is Redis running?");
}, false);