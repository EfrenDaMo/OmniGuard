// Espera a que el contenido del DOM se cargue por completo
document.addEventListener("DOMContentLoaded", function() {
    // Se asegura que ciertas cosas pasen solo si se puede verificar la sesión
    fetch("/api/session", {
        method: "GET",
        credentials: "include",
    }).then(response => response.json()).then(data => {
        if (!data.success) {
            window.location.href = "/login";
        } else {
            const userAvatar = document.getElementById("userAvatar");
            if (userAvatar && data.usuario) {
                userAvatar.textContent = data.usuario.nombre.charAt(0).toUpperCase();
            }
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
});
