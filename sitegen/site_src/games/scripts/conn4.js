function getDifficulty() {
    var inputs = document.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {
        var input = inputs[i];

        if (input.type === "radio" && input.checked) {
            return input.value;
        }
    }
}

const consol = document.getElementById("game_out");

consol.innerHTML = "";

consol.innerHTML += getDifficulty();


