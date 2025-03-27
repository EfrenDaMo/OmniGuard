// Espera a que el contenido del DOM se cargue por completo
document.addEventListener("DOMContentLoaded", function() {
    const userAvatar = document.getElementById("userAvatar");
    const userTableBody = document.getElementById("userTableBody");

    // Se asegura que ciertas cosas pasen solo si se puede verificar la sesión
    function cargarUsuarios() {
        fetch(`/api/users?timestamp=${new Date().getTime()}`, {
            method: "GET",
            credentials: "include"
        }).then(response => response.json()).then(data => {
            if (data.success && userTableBody) {
                userTableBody.innerHTML = "";

                data.usuarios.forEach((usuario, index) => {
                    const originalPasswordLength = Math.max(8, Math.min(22, Math.floor(usuario.password.length / 4))) / 2

                    const row = document.createElement('tr')
                    const td1 = document.createElement('td')
                    const td2 = document.createElement('td')
                    const td3 = document.createElement('td')
                    const td4 = document.createElement('td')
                    const td5 = document.createElement('td')

                    td1.textContent = index + 1
                    td2.textContent = usuario.id
                    td3.textContent = usuario.nombre

                    const password = document.createElement('span')
                    password.className = "password-mask"
                    password.dataset.originalLength = originalPasswordLength
                    password.textContent = "*".repeat(originalPasswordLength)

                    const eye_btn = document.createElement('button')
                    eye_btn.id = "btn-eye"
                    eye_btn.className = "btn"
                    eye_btn.dataset.id = usuario.id
                    eye_btn.dataset.visible = "false"
                    eye_btn.dataset.timeout = ""
                    eye_btn.textContent = "👁️"

                    td4.appendChild(password)
                    td4.appendChild(eye_btn)

                    const edt_btn = document.createElement('button')
                    edt_btn.id = "btn-edt"
                    edt_btn.className = "btn"
                    edt_btn.dataset.id = usuario.id
                    edt_btn.textContent = "✏️"

                    const del_btn = document.createElement('button')
                    del_btn.id = "btn-del"
                    del_btn.className = "btn"
                    del_btn.dataset.id = usuario.id
                    del_btn.textContent = "🗑️"

                    td5.appendChild(edt_btn)
                    td5.appendChild(del_btn)

                    row.appendChild(td1)
                    row.appendChild(td2)
                    row.appendChild(td3)
                    row.appendChild(td4)
                    row.appendChild(td5)

                    userTableBody.appendChild(row)
                });
            }
        }).catch(error => {
            console.error("Error verificando sesión:", error);
            window.location.href = "/login";
        });
    }

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

            cargarUsuarios()
        }
    }).catch(error => {
        console.error("Error verificando sesión:", error);
        window.location.href = "/login";
    });

    document.getElementById("newUserLink").addEventListener("click", function() {
        fetch("/api/session", {
            method: "GET",
            credentials: "include"
        }).then(response => response.json()).then(data => {
            if (data.success) {
                window.location.href = "/create-user"
            } else {
                alert(data.message)
            }
        }).catch(error => {
            console.error("Error verificando sesión:", error);
            window.location.href = "/login";
        });
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
        if (e.target.id === 'btn-eye') {
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

    window.addEventListener('focus', function() {
        cargarUsuarios()
    })
});
