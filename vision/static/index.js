function getContainerCookies(cname) {
    // Try to get Vision cookies, and if they exist, use content to add containers to page.
    const name = cname + "=";
    const cDecoded = decodeURIComponent(document.cookie);
    const cArr = cDecoded.split('; ');
    let res;
    cArr.forEach(val => {
        if (val.indexOf(name) === 0) res = val.substring(name.length);
    })
    return res
};

function setContainerCookies(cname, action, data) {
    // If a cookie doesn't exist, make a new one, but if one does exist, change it's contents.
    var container = data.split(':');
    const now = new Date();
    const time = now.getTime();
    const expireTime = time + 1000 * 36000;
    now.setTime(expireTime);
    var expires = `expires=${now.toUTCString()}`;
    var path = "path=/";
    if (getContainerCookies(cname)) {
        var containers = JSON.parse(getContainerCookies(cname));
        if (action == "ADD") {
            containers.push(`${container[0]}:${container[1]}`);
            document.cookie = `${cname}=${JSON.stringify(containers)};${expires};${path}`;
        } else if (action == "REMOVE") {
            for (i = 0; i < containers.length; i++) {
                if (containers[i] == data) {
                    containers.splice(i, 1);
                    break;
                }
            }
            document.cookie = `${cname}=${JSON.stringify(containers)};${expires};${path}`;
        }
    } else {
        document.cookie = `${cname}=${JSON.stringify([data])};${expires};${path}`;
    }
};

function addSource(name, containerId) {
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

function addSourceForm(form) {
    // Add a Source textarea based on a provided drop down to select from.
    const newSource = JSON.parse(form.sources.value);
    const newSourceName = newSource["Name"];
    const newSourceId = newSource["ContainerId"];

    if (newSource == "NONE") {
        return null
    } else if (document.getElementById(`${newSourceName}:${newSourceId}-container`)) {
        // If a text area exists for what was selected, do nothing.
        return null
    } else {
        addSource(newSourceName, newSourceId);
        setContainerCookies("vision-containers", "ADD", `${newSourceName}:${newSourceId}`);
    };
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

function removeSource(elem, data) {
    // Remove a textarea from the page.
    const sourceBox = document.getElementById(elem);
    sourceBox.remove();
    setContainerCookies("vision-containers", "REMOVE", data);
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
    const myTextArea = document.getElementById(elm);
    myTextArea.textContent = '';
};

window.onload = function () {
    if (getContainerCookies("vision-containers")) {
        var containers = JSON.parse(getContainerCookies("vision-containers"));
        for (i = 0; i < containers.length; i++) {
            var container = containers[i].split(':');
            addSource(container[0], container[1]);
        };
    };
};
