const toggle = document.querySelector('#toggle'); 
const password_v = document.querySelector('#password');

  toggle.addEventListener("click", () => {
    if (password_v.type == "password") {
      password_v.type = "text";
      toggle.classList.replace('bi-eye', 'bi-eye-slash');
    }
    else {
      password_v.type = "password";
      toggle.classList.replace('bi-eye-slash', 'bi-eye');
    }
  });  

