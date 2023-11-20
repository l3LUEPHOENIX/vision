document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const loginButton = document.getElementById("login-button");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    form.addEventListener("submit", function (event) {
        const username = usernameInput.value;
        const password = passwordInput.value;

        if (username.length > 30 || password.length > 30) {
            event.preventDefault(); // Prevent the form from submitting
            alert("Both fields should be 30 characters or less.");
        }
        // You can add additional validation or submit logic here.
    });
});
