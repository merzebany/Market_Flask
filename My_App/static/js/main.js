
document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("toggle");
    const password = document.getElementById("password"); // Make sure this exists too
    
    toggle.addEventListener("click", () => {
        if (password.type == "password") {
            password.type = "text";
            toggle.classList.replace('bi-eye', 'bi-eye-slash');
        } else {
            password.type = "password";
            toggle.classList.replace('bi-eye-slash', 'bi-eye');
        }
    });
});