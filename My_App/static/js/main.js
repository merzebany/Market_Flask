
const password = document.getElementById("password")

const toggle = document.getElementById("toggle")

toggle.addEventListener("click", () => {
  if (password.type == "password") {
    password.type = "text";
    toggle.classList.replace('bi-eye', 'bi-eye-slash');
  }
  else {
     password.type = "password";
     toggle.classList.replace('bi-eye-slash', 'bi-eye' );
  }
      
})