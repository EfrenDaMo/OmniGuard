// Espera a que el contenido del DOM se cargue por completo
document.addEventListener("DOMContentLoaded", function() {
    const userAvatar = document.getElementById("userAvatar");
    const userTableBody = document.getElementById("userTableBody");

    // Se asegura que ciertas cosas pasen solo si se puede verificar la sesión
    fetch("/api/session", {
        method: "GET",
        credentials: "include",
    }).then(response => response.json()).then(data => {
        if (!data.success) {
            // Si no hay sesión activa se redirige al login
            window.location.href = "/login";
        } else {
            // Actualiza informacion del usuario
            if (userAvatar && data.usuario) {
                userAvatar.textContent = data.usuario.nombre.charAt(0).toUpperCase();
            }

            return fetch("/api/users", {
                method: "GET",
                credentials: "include"
            });
        }
    }).then(response => response.json()).then(data => {
        if (data.success && userTableBody) {
            userTableBody.innerHTML = "";

            data.usuarios.forEach((usuario, index) => {
                const originalPasswordLength = Math.max(8, Math.min(22, Math.floor(usuario.password.length / 4))) / 2

                const row = document.createElement('tr')
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${usuario.id}</td>
                    <td>${usuario.nombre}</td>
                    <td>
                        <span class="password-mask" data-original-length="${originalPasswordLength}">
                            ${"*".repeat(originalPasswordLength)}
                        </span>
                        <button class="btn-eye" data-id="${usuario.id}" data-visible="false" data-timeout="">👁️</button>
                    </td>
                `;

                /*
                <td>
                   <button class="btn-editar" data-id"${usuario.id}">Editar</button>
                   <button class="btn-eliminar" data-id"${usuario.id}">Eliminar</button>
                </td>
                */
                userTableBody.appendChild(row)
            });
        }
    }).catch(error => {
        console.error("Error verificando sesión:", error);
        window.location.href = "/login";
    });

    // Función de termino de sesión
    // Se ejecuta al hacer clic en el botón de cerrar sesión
    document.getElementById("logoutBtn").addEventListener("click", function() {
        fetch('/api/logout', {
            method: "POST",
            credentials: "include"
        }).then(response => response.json()).then(data => {
            if (data.success) {
                window.location.href = "/login";
            } else {
                alert("No se pudo cerrar la sesión");
            }
        }).catch(error => {
            console.error("Error:", error);
            alert("Ocurrio un error al cerrar la sesión");
        });
    });


    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('btn-eye')) {
            const btn = e.target;
            const userId = e.target.dataset.id;
            const passwordSpan = e.target.previousElementSibling;
            const isVisible = btn.dataset.visible === 'true';
            const originalLength = parseInt(passwordSpan.dataset.originalLength)
            let timeoutID;

            try {
                if (!isVisible) {
                    btn.disabled = true;
                    btn.textContent = '...';

                    const response = await fetch(`/api/users/decrypt-password/${userId}`, {
                        method: "GET",
                        credentials: "include"
                    });

                    const data = await response.json()

                    if (data.success) {
                        passwordSpan.textContent = data.password;
                        btn.textContent = "🔒";
                        btn.dataset.visible = 'true';

                        timeoutID = setTimeout(() => {
                            passwordSpan.textContent = "*".repeat(originalLength);
                            btn.textContent = "👁️";
                            btn.dataset.visible = 'false';
                        }, 30000);
                    } else {
                        alert('Error: ' + data.message);
                        btn.textContent = '👁️';
                        btn.disabled = false;
                    }
                } else {
                    passwordSpan.textContent = '*'.repeat(originalLength);
                    btn.textContent = '👁️';
                    btn.dataset.visible = 'false';
                    clearTimeout(timeoutID);
                }
            } catch (err) {
                console.error("Decrypt error:", err)
                btn.textContent = '👁️';
                btn.disabled = false;
            } finally {
                btn.disabled = false;

                if (timeoutID) btn.dataset.timeout = timeoutID;
            }
        }
    });
});
