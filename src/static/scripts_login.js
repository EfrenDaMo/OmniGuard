// Función de inicio de sesión
// Se ejecuta al hacer clic en el botón de inicio de sesión
document.getElementById('loginBtn').addEventListener('click', function() {
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const recaptchaResponse = grecaptcha.getResponse();
    const recaptchaError = document.getElementById('recaptchaError');
    
    // Validar campos vacíos
    if (!name || !password) {
        alert('Por favor, completa todos los campos');
        return;
    }
    
    // Validar reCAPTCHA
    if (!recaptchaResponse) {
        recaptchaError.style.display = 'block';
        return;
    } else {
        recaptchaError.style.display = 'none';
    }
    
    // Aquí iría la lógica para validar el login
    console.log('Intentando login con:', name, password);
    console.log('Respuesta reCAPTCHA:', recaptchaResponse);
    
    //aquí iría la lógica para validar el login y el recaptcha
    
    // Limpiar formulario después del login
    document.getElementById('name').value = '';
    document.getElementById('password').value = '';
    grecaptcha.reset();
});

//document.getElementById('createAccountBtn').addEventListener('click', function() {
    // Redirección a página de creación de cuenta
//});