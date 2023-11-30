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

function clearTextarea(elm) {
    // Clear all text out of the given textarea.
    const myTextArea = document.getElementById(elm);
    myTextArea.textContent = '';
};

function removeSource(source_displayname) {
    // Remove a textarea from the page.
    var current_location = window.location.href;
    return window.location.assign(current_location.replace(`/${source_displayname}`, ''));
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

function filterList(list_name, query) {
    var list = document.getElementById(list_name).rows;
    if (!query || query.trim() === '') {
        for (x = 0; x < list.length; x++) {
            list[x].style.display = '';
        }
    } else {
        for (x = 0; x < list.length; x++) {
            if (!(RegExp('^' + query.replace(/\*/g, '.*') + '$').test(list[x].id))) {
                list[x].style.display = 'none';
            } else {
                list[x].style.display = '';
            }
        }
    }
}

function submitFileQuery(source_displayname) {
    event.preventDefault();
    const form = document.getElementById(`${source_displayname}-form`);
    const formData = new FormData(form);
    
    fetch(window.location.href, {
        method: "POST",
        headers: new Headers({
            "Content-type":"application/json",
            "X-CSRFToken": formData.get('csrf_token')
        }),
        body: JSON.stringify({
            source: source_displayname,
            query_type: formData.get('query_type'),
            query: String(formData.get('query')),
            files: formData.getAll('file')
        })
    });
}

function selectAllCheckbox(source_displayname) {
    var table = document.getElementById(`${source_displayname}-table`);
    var checkboxes = table.querySelectorAll('input[type="checkbox"]');
    var selectAll = document.getElementById(`${source_displayname}-selection`);

    if (selectAll.checked) {
        checkboxes.forEach(function (currentValue, index, arr) {
            if (currentValue.closest('tr').style.display !== 'none') {
                currentValue.checked = true;
            }
        });
    } else {
        checkboxes.forEach(function (currentValue, index, arr) {
            currentValue.checked = false;
        });
    }
}

// Create all listeners for the textareas on the page.
window.onload = function () {
    const source_containers = document.querySelectorAll("div[id$='-container'].grid-item");
    source_containers.forEach(function(currentValue, index, arr) {
        var source_displayname = currentValue.id.split('-')[0];
        const newListenerScript = `
        var ${source_displayname}_source_listener = new EventSource('/stream?channel=${source_displayname}:archivist');
        ${source_displayname}_source_listener.addEventListener('event', function(event) {
            var data = JSON.parse(event.data);
            var sourceTextArea = document.getElementById('${source_displayname}-textarea');
            if (sourceTextArea) {
                sourceTextArea.textContent += \`\$\{event.data\}\\n\`;
                if (document.getElementById('${source_displayname}-checkbox').checked) {
                    sourceTextArea.scrollTop = sourceTextArea.scrollHeight;
                }
            }
        }, false);
        `
        var newScriptElement = document.createElement("script");
        var inlineScript = document.createTextNode(newListenerScript);
        newScriptElement.appendChild(inlineScript);
        currentValue.appendChild(newScriptElement);
    });
}