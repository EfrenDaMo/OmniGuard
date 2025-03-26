//sirve para validar el formulario de creación de usuario
document.addEventListener('DOMContentLoaded', function() { 
    const form = document.getElementById('userForm'); //formulario
    const fullnameInput = document.getElementById('fullname'); //nombre
    const passwordInput = document.getElementById('password'); //contraseña
    const passwordError = document.getElementById('passwordError'); //error de contraseña
    const successMessage = document.getElementById('successMessage'); //mensaje de éxito

    // Validación de contraseña
    passwordInput.addEventListener('input', function() {
        if (passwordInput.value.length >= 8) {
            passwordError.style.display = 'none';
            passwordInput.style.borderColor = 'var(--success-color)';
        } else {
            passwordError.style.display = 'block';
            passwordInput.style.borderColor = 'var(--error-color)';
        }
    });

    // Envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validación final
        if (passwordInput.value.length < 8) {
            passwordError.style.display = 'block';
            passwordInput.style.borderColor = 'var(--error-color)';
            passwordInput.focus();
            return;
        }
        
        // Aca enviar los datos al servidor
        console.log('Usuario creado:', {
            nombre: fullnameInput.value,
            password: passwordInput.value
        });
        
        // Mostrar mensaje de éxito
        form.style.display = 'none'; //ocultar formulario
        successMessage.style.display = 'block'; //mostrar mensaje de éxito

        // Limpiar campos del formulario
        fullnameInput.value = '';
        passwordInput.value = '';
        
    });
});