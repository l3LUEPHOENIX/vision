function formSubmit(form) {
    // var textInput = form.text-input.value;
    alert('submitted');
}

function copyToClipboard(elm) {
    const input = elm.parentNode.getElementsByTagName('input');
    navigator.clipboard.writeText(input[0].value);
}

function addTextinput(elm) {
    const containeridRow = elm.parentNode.parentNode.getElementsByClassName('grid-container')[0];
    const rowID = elm.parentNode.parentNode.getAttribute('id');
    const newTextinput = document.createElement('input');
    var itemCount = containeridRow.getElementsByTagName('input').length;
    // var newTextinput = `<input form="edp-provision" type="text" id="containerId_${itemCount + 1}" name="containerId_${itemCount + 1}" value="new-container-id">`
    
    newTextinput.type = "text";
    newTextinput.id = `containerId_${itemCount + 1}`;
    newTextinput.name = `containerId_${itemCount + 1}`;
    newTextinput.value = "new-container";
    newTextinput.setAttribute("form",`${rowID}-form`);

    containeridRow.appendChild(newTextinput);
    // parentRow.innerHTML += newTextinput;
}

function applyChanges(form) {
    form.submit();
}

function deleteRow(elm) {
    // Get the actionType field and set the value to DELETE and remove all elements.
    const thisRowInputs = elm.parentNode.parentNode.getElementsByTagName("input");
    const actionType = thisRowInputs[thisRowInputs.length - 1];

    actionType.setAttribute('value','DELETE');
    document.getElementById(elm.getAttribute('form')).submit();
    elm.parentNode.parentNode.remove();
}