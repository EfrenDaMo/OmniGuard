document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('id');
    let currentName = '';

    // DOM Elements
    const form = document.getElementById('userForm');
    const fullnameInput = document.getElementById('fullname');
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    const successMessage = document.getElementById('successMessage');

    // Fetch user data
    fetch('/api/users').then(response => {
        if (!response.ok) {
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        return response.json();
    }).then(data => {
        if (data.success) {
            const user = data.usuarios.find(u => u.id === parseInt(userId));
            if (user) {
                currentName = user.nombre;
                fullnameInput.value = user.nombre;
            }
        }
    });

    // Password validation
    passwordInput.addEventListener('input', function() {
        const isValid = passwordInput.value.length >= 8 || passwordInput.value === '';
        passwordError.style.display = isValid ? 'none' : 'block';
        passwordInput.style.borderColor = isValid ? 'var(--success-color)' : 'var(--error-color)';
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const newName = fullnameInput.value.trim();
        const newPassword = passwordInput.value;

        // Validation
        if (!newName) {
            fullnameInput.style.borderColor = 'var(--error-color)';
            return;
        }

        if (newPassword && newPassword.length < 8) {
            passwordError.style.display = 'block';
            passwordInput.style.borderColor = 'var(--error-color)';
            return;
        }

        // Prepare update data
        const updateData = {
            nombre_actual: currentName,
            nuevo_nombre: newName,
            nueva_password: newPassword
        };

        // Send update request
        fetch('/api/users/update', {
            method: 'PUT',
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(updateData)
        }).then(response => response.json()).then(data => {
            if (data.success) {
                form.style.display = 'none';
                successMessage.style.display = 'block';
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                alert(data.message || "Error al actualizar el usuario");
            }
        }).catch(error => {
            console.error("Error:", error);
            alert("Ocurrió un error al actualizar el usuario");
        });
    });
});
