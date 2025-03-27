// Espera a que el contenido del DOM se cargue por completo
document.addEventListener("DOMContentLoaded", function() {
    // Obtener elementos de la pagina
    const logoutBtn = document.getElementById("logoutBtn");
    const userAvatar = document.getElementById("userAvatar");
    const newUserLink = document.getElementById("newUserLink");
    const userTableBody = document.getElementById("userTableBody");

    // Validar elementos esenciales
    if (!userTableBody || !newUserLink || !logoutBtn) {
        console.error("Elementos esenciales faltan en el DOM")
        return;
    }

    // Se asegura que ciertas cosas pasen solo si se puede verificar la sesión
    function cargarUsuarios() {
        fetch(`/api/users?timestamp=${Date.now()}`, {
            method: "GET",
            credentials: "include"
        }).then(response => {
            if (!response.ok) throw new Error("HTTP error " + response.status);
            return response.json();
        }).then(data => {
            if (data.success && userTableBody) {
                userTableBody.innerHTML = "";

                data.usuarios.forEach((usuario, index) => {
                    const row = document.createElement('tr');
                    const passwordLength = Math.max(8, Math.min(22, Math.floor(usuario.password.length / 4))) / 2;

                    const cells = Array.from({ length: 5 }, () => document.createElement('td'));

                    cells[0].textContent = index + 1;
                    cells[1].textContent = usuario.id;
                    cells[2].textContent = usuario.nombre;

                    const passwordSpan = document.createElement('span');
                    passwordSpan.className = "password-mask";
                    passwordSpan.dataset.originalLength = passwordLength;
                    passwordSpan.textContent = "*".repeat(passwordLength);

                    const eyeBtn = document.createElement('button');
                    eyeBtn.id = "btn-eye";
                    eyeBtn.className = "btn";
                    eyeBtn.dataset.id = usuario.id;
                    eyeBtn.dataset.visible = "false";
                    eyeBtn.dataset.timeout = "";
                    eyeBtn.textContent = "👁️";

                    cells[3].append(passwordSpan, eyeBtn)

                    const edtBtn = document.createElement('button');
                    edtBtn.id = "btn-edt";
                    edtBtn.className = "btn";
                    edtBtn.dataset.id = usuario.id;
                    edtBtn.textContent = "✏️";

                    const delBtn = document.createElement('button');
                    delBtn.id = "btn-del";
                    delBtn.className = "btn";
                    delBtn.dataset.id = usuario.id;
                    delBtn.textContent = "🗑️";

                    cells[4].append(edtBtn, delBtn)


                    row.append(...cells);
                    userTableBody.appendChild(row)
                });
            }
        }).catch(error => {
            console.error("Error cargando usuarios", error);
            window.location.href = "/login";
        });
    }

    // Verificar si se activo la sesion
    fetch("/api/session", {
        method: "GET",
        credentials: "include",
    }).then(response => {
        if (!response.ok) throw new Error("Fallo el checado de sesión");
        return response.json()
    }).then(data => {
        if (!data.success) {
            // Si no hay sesión activa se redirige al login
            window.location.href = "/login";
        }

        // Actualiza informacion del usuario
        if (userAvatar && data.usuario) {
            userAvatar.textContent = data.usuario.nombre.charAt(0).toUpperCase();
        }

        cargarUsuarios()
    }).catch(error => {
        console.error("Error verificando sesión:", error);
        window.location.href = "/login";
    });

    newUserLink.addEventListener("click", function() {
        fetch("/api/session", {
            method: "GET",
            credentials: "include"
        }).then(response => {
            if (!response.ok) throw new Error("Fallo el checado de sesión");
            return response.json();
        }).then(data => {
            window.location.href = data.success ? "/create-user" : "/login";
        }).catch(error => {
            console.error("Error verificando sesión:", error);
            window.location.href = "/login";
        });
    });

    // Función de termino de sesión
    // Se ejecuta al hacer clic en el botón de cerrar sesión
    logoutBtn.addEventListener("click", function() {
        fetch('/api/logout', {
            method: "POST",
            credentials: "include"
        }).then(response => {
            if (!response.ok) throw new Error("Fallo el cierre de sesión");
            return response.json();
        }).then(data => {
            window.location.href = data.success ? "/login" : window.location.href;
        }).catch(error => {
            console.error("Error al cerrar session:", error);
            alert("Ocurrio un error al cerrar la sesión");
        });
    });


    document.addEventListener('click', async (e) => {
        if (e.target.id === 'btn-eye') {
            const btn = e.target;
            const userId = e.target.dataset.id;
            const passwordSpan = e.target.previousElementSibling;
            const isVisible = btn.dataset.visible === 'true';
            const originalLength = parseInt(passwordSpan.dataset.originalLength, 10)

            try {
                if (!isVisible) {
                    btn.disabled = true;
                    btn.textContent = '...';

                    const response = await fetch(`/api/users/decrypt-password/${userId}`, {
                        method: "POST",
                        credentials: "include"
                    });

                    if (!response.ok) throw new Error("Fallo el mostrado de la contraseña");
                    const data = await response.json();

                    passwordSpan.textContent = data.password;
                    btn.textContent = "🔒";
                    btn.dataset.visible = 'true';

                    const timeoutID = setTimeout(() => {
                        passwordSpan.textContent = "*".repeat(originalLength);
                        btn.textContent = "👁️";
                        btn.dataset.visible = 'false';
                    }, 30000);

                    btn.dataset.timeout = timeoutID;
                } else {
                    clearTimeout(Number(btn.dataset.timeout));
                    passwordSpan.textContent = '*'.repeat(originalLength);
                    btn.textContent = '👁️';
                    btn.dataset.visible = 'false';
                }
            } catch (error) {
                console.error("Decrypt error:", error)
                alert("Error al mostrar la contraseña")
            } finally {
                btn.disabled = false;
            }
        }
    });

    window.addEventListener('focus', cargarUsuarios);
});
