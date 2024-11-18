/**
 * Toggle whether a description (e.g. in a div) is displayed or not
 *
 * @param descriptionId The element ID of the element containing the description text, e.g. a div
 * @param btnId The element of the button which triggers this function, the text of this button will be changed
 *              accordingly
 * @param inputId The ID of an input element that should be set to true if the description has been
 *                toggled at least once
 */
function toggleDescription(descriptionId, btnId, inputId) {
    let description = document.getElementById(descriptionId);
    let btn = document.getElementById(btnId);
    if (inputId != null) {
        let input = document.getElementById(inputId);
        input.value = "True";
    }

    if (window.getComputedStyle(description).maxHeight === "0px") {
        description.style.maxHeight = "20cm";
        description.style.overflowY = "scroll";
        btn.innerHTML = "Hide task description";
    } else {
        description.style.maxHeight = "0px";
        btn.innerHTML = "Show task description";
        description.style.overflowY = "hidden";
    }
}