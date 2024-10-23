var inputs = document.querySelectorAll('input[type="submit"]');
inputs.forEach(function(input) {
    if (input.disabled === true ) {
    input.setAttribute("class", "go-back__button-disabled");
    }
});

