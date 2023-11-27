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

function removeSource(elem) {
    // Remove a textarea from the page.
    document.getElementById(elem).remove();
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
    if (query.value == '') {
        for (x = 0; x < list.length; x++) {
            list[x].style.visibility = 'visible';
        }
    } else {
        for (x = 0; x < list.length; x++) {
            if (!(RegExp('^' + query.replace(/\*/g, '.*') + '$').test(list[x].id))) {
                list[x].style.visibility = 'hidden';
            } else {
                list[x].style.visibility = 'visible';
            }
        }
    }
}