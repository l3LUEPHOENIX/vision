function addArchivistSourceForm(form) {
    // Add a Source textarea based on a provided drop down to select from.
    const newSource = form.sources.value;

    if (newSource == "NONE") {
        // If the blank option is selected, do nothing.
        return null
    } else {
        return window.location.assign(`${window.location.href}/${newSource}`);
    };
};

function addArchivistSourceFeed(name, containerId) {
    var newBox = `
        <div id="${name}:${containerId}-container" class="grid-item">
            <div class="grid-item-header">
                <div class="grid-item-header-title">${name}:${containerId}</div>
                <div class="grid-item-header-checkbox-container">
                    <label for="checkbox" class="grid-item-header-checkbox-label">Follow</label>
                    <input id="${name}:${containerId}-checkbox" type="checkbox" class="grid-item-header-checkbox">
                </div>
                <div class="grid-item-header-button-container">
                    <button onClick="clearTextarea('${name}:${containerId}')" class="grid-item-header-button">Clear</button>
                    <button onClick="downloadText('${name}:${containerId}')" class="grid-item-header-button">Download</button>
                    <button onClick="removeSource('${name}:${containerId}-container','${name}:${containerId}')" class="grid-item-header-button">Remove</button>
                </div>
            </div>
            <textarea id="${name}:${containerId}" class="grid-item-body" cols="80" rows="50" readonly="true" wrap="true"></textarea>
        </div>
    `;
    var newListenerScript = `
        var ${name}_${containerId}_source = new EventSource("/stream?channel=${name}:${containerId}");
        ${name}_${containerId}_source.addEventListener('event', function(event) {  
            var data = JSON.parse(event.data);
            if (document.getElementById('${name}:${containerId}')) {
                document.getElementById('${name}:${containerId}').textContent += \`\$\{data.message\}\\n\`;
                if (document.getElementById('${name}:${containerId}-checkbox').checked) {
                    document.getElementById('${name}:${containerId}').scrollTop = document.getElementById('${name}:${containerId}').scrollHeight;
                }
            };
        }, false);
        ${name}_${containerId}_source.addEventListener('error', function(event) {
            console.log("Failed to connect to event stream. Is Redis running?");
        }, false);
    `;
    document.getElementById("data-container").innerHTML += newBox;
    var newScriptElement = document.createElement("script");
    var inlineScript = document.createTextNode(newListenerScript);
    newScriptElement.appendChild(inlineScript);
    document.getElementById(`${name}:${containerId}-container`).appendChild(newScriptElement);
}

function clearTextarea(elm) {
    // Clear all text out of the given textarea.
    const myTextArea = document.getElementById(elm);
    myTextArea.textContent = '';
};

function removeSource(elem, data) {
    // Remove a textarea from the page.
    const sourceBox = document.getElementById(elem);
    sourceBox.remove();
    setContainerCookies("vision-containers", "REMOVE", data);
};

function downloadText(elm) {
    const myTextArea = document.getElementById(elm);
    const date = new Date();
    const file_name = `${myTextArea.id}-${date.getMonth()}-${date.getDay()}-${date.getFullYear()}`;

    // Create element with <a> tag
    const link = document.createElement("a");

    // Create a blog object with the file content which you want to add to the file
    const file = new Blob([myTextArea.textContent], { text: 'text/plain' });

    // Add file content in the object URL
    link.href = URL.createObjectURL(file);

    // Add file name
    link.download = `${file_name}.txt`;

    // Add click event to <a> tag to save file.
    link.click();
    URL.revokeObjectURL(link.href);
};

function changeFontSize(size) {
    // Change the fontsize for all textareas in the document.
    var myTextAreas = document.getElementsByTagName("textarea")
    for (i = 0; i < myTextAreas.length; i++) {
        myTextAreas[i].style.fontSize = size;
    };
};
