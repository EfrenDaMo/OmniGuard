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
        fetch("/api/registro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nombre: fullnameInput.value,
                password: passwordInput.value,
            }),
            credentials: "include"
        }).then(response => response.json()).then(data => {
            if (data.success) {
                form.style.display = 'none'; //ocultar formulario
                successMessage.style.display = 'block'; //mostrar mensaje de éxito

                successMessage.innerHTML += "<p>Serás redirigido al dashboard en 5 segundos...</p>"

                // Limpiar campos del formulario
                fullnameInput.value = '';
                passwordInput.value = '';

                setTimeout(() => {
                    window.location.href = '/dashboard?timestamp=' + new Date().getTime();
                }, 5000);
            } else {
                alert(data.message || "Error al crear el usuario");
            }
        }).catch(error => {
            console.error("Error:", error);
            alert("Ocurrio un error al crear el usuario")
        });
    });
});