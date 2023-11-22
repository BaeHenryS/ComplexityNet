function fillText(text) {
    // Get the textarea element by its id
    var textarea = document.getElementById('chat-input');

    // Set the value of the textarea
    textarea.textContent = text;
}



function pressButton() {
    // Get the div element by its class
    var div = document.querySelector('.MuiInputAdornment-root.MuiInputAdornment-positionEnd.MuiInputAdornment-standard.MuiInputAdornment-sizeMedium.css-1gdcidm');

    // Get the button within the div
    var button = div.querySelector('button');

    // Simulate a click on the button
    button.click();
}



<textarea aria-invalid="false" autocomplete="false" id="chat-input" placeholder="Type your message here..." class="MuiInputBase-input MuiInput-input MuiInputBase-inputMultiline MuiInputBase-inputAdornedStart MuiInputBase-inputAdornedEnd css-o0s11j" style="height: 24px; overflow: hidden;"></textarea>


<textarea aria-invalid="false" autocomplete="false" id="chat-input" placeholder="Type your message here..." class="MuiInputBase-input MuiInput-input MuiInputBase-inputMultiline MuiInputBase-inputAdornedStart MuiInputBase-inputAdornedEnd css-o0s11j" style="height: 24px; overflow: hidden;">Hello</textarea>