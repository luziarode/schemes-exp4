/**
 *  Ensure that only questions/input fields are shown in the survey
 *  [Demographics.html]{@link payment_schemes_exp3/Demographics.html} that make logically sense.
 *
 *  E.g. the input field for 'Other' is not available if one of the given options has been selected
 */

// Logic for gender question:
const genderOtherInput = document.getElementById("id_other_gender");
const genderOtherLabel = document.querySelector("label[for=id_other_gender]");

function hideGenderOtherInput() {
    genderOtherInput.style.display = "none";
    genderOtherLabel.style.display = "none";
    genderOtherInput.value = "";
}
function showGenderOtherInput() {
    genderOtherInput.style.display = "inline";
    genderOtherLabel.style.display = "inline";
}
hideGenderOtherInput();

for (const i of Array(2).keys()) {
  let genderI = document.getElementById(`id_gender-${i}`);
  genderI.onclick = hideGenderOtherInput;
}
let genderI = document.getElementById("id_gender-3");
genderI.onclick = hideGenderOtherInput;
const genderOther = document.getElementById("id_gender-2");
genderOther.onclick = showGenderOtherInput;

// Logic for ethnicity question:
const ethnicityOtherInput = document.getElementById("id_other_ethnicity");
const ethnicityOtherLabel = document.querySelector("label[for=id_other_ethnicity]");
function hideEthnicityOtherInput() {
    ethnicityOtherInput.style.display = "none";
    ethnicityOtherLabel.style.display = "none";
    ethnicityOtherInput.value = "";
}
function showEthnicityOtherInput() {
    ethnicityOtherInput.style.display = "inline";
    ethnicityOtherLabel.style.display = "inline";
}
hideEthnicityOtherInput();

for (const i of Array(4).keys()) {
  let ethnicityI = document.getElementById(`id_ethnicity-${i}`);
  ethnicityI.onclick = hideEthnicityOtherInput;
}
let ethnicityI = document.getElementById("id_ethnicity-5");
ethnicityI.onclick = hideEthnicityOtherInput;
const ethnicityOther = document.getElementById("id_ethnicity-4");
ethnicityOther.onclick = showEthnicityOtherInput;


// Logic for political orientation question:
const partyOtherInput = document.getElementById("id_other_political");
const partyOtherLabel = document.querySelector("label[for=id_other_political]");
function hidePartyOtherInput() {
    partyOtherInput.style.display = "none";
    partyOtherLabel.style.display = "none";
    partyOtherInput.value = "";
}
function showPartyOtherInput() {
    partyOtherInput.style.display = "inline";
    partyOtherLabel.style.display = "inline";
}
hidePartyOtherInput();

for (const i of Array(3).keys()) {
  let partyI = document.getElementById(`id_political_orientation-${i}`);
  partyI.onclick = hidePartyOtherInput;
}
let partyI = document.getElementById("id_political_orientation-4");
partyI.onclick = hidePartyOtherInput;
const partyOther = document.getElementById("id_political_orientation-3");
partyOther.onclick = showPartyOtherInput;

// Logic for home state question:
const inUSAYes =  document.getElementById("id_residence_in_us-0");
const inUSANo =  document.getElementById("id_residence_in_us-1");
const inUSANoAnswer = document.getElementById("id_residence_in_us-2");
const whichState = document.getElementById("id_state");

inUSAYes.onclick = () => {
    whichState.disabled = false;
};
inUSANo.onclick = () => {
    whichState.disabled = true;
    whichState.value = "--------";
};

inUSANoAnswer.onclick = () => {
    whichState.disabled = true;
    whichState.value = "--------";
};
