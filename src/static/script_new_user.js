// Sirve para validar el formulario de creación de usuario
document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const form = document.getElementById('userForm'); //formulario
    const fullnameInput = document.getElementById('fullname'); //nombre
    const passwordInput = document.getElementById('password'); //contraseña
    const passwordError = document.getElementById('passwordError'); //error de contraseña
    const successMessage = document.getElementById('successMessage'); //mensaje de éxito

    // Validar elementos esenciales
    if (!form || !fullnameInput || !passwordInput || !passwordError || !successMessage) {
        console.error("Elementos esenciales faltantes en el formulario");
        return;
    }

    // Validación de contraseña
    passwordInput.addEventListener('input', function() {
        const isValid = passwordInput.value.length >= 8;

        passwordError.style.display = isValid ? 'none' : 'block';
        passwordInput.style.borderColor = isValid ? 'var(--success-color)' : 'var(--error-color)';
    });

    // Envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validación final
        if (!fullnameInput.value.trim() || passwordInput.value.length < 8) {
            if (!fullnameInput.value.trim()) {
                fullnameInput.style.borderColor = 'var(--error-color)';
                fullnameInput.focus();
            }
            if (passwordInput.value.length < 8) {
                passwordError.style.display = 'block';
                passwordInput.style.borderColor = 'var(--error-color)';
                passwordInput.focus();
            }
            return;
        }

        // Enviar los datos al servidor
        fetch("/api/registro", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                nombre: fullnameInput.value,
                password: passwordInput.value,
            }),
        }).then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);;
            return response.json();
        }).then(data => {
            if (data.success) {
                form.style.display = 'none'; //ocultar formulario
                successMessage.style.display = 'block'; //mostrar mensaje de éxito

                const redirectMsg = document.createElement('p');
                redirectMsg.textContent = "Serás redirigido al dashboard en 5 segundos...";

                successMessage.appendChild(redirectMsg);

                // Limpiar campos del formulario
                form.reset();

                setTimeout(() => {
                    window.location.href = `/dashboard?timestamp=${Date.now()}`;
                }, 5000);
            } else {
                alert(data.message || "Error al crear el usuario");
            }
        }).catch(error => {
            console.error("Error:", error);
            alert("Ocurrió un error al crear el usuario")
        });
    });
});