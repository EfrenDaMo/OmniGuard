/**
 * Autenticación de Usuarios con reCAPTCHA
 * 
 * Controla el proceso de login con:
 * - Validación de campos obligatorios
 * - Integración con reCAPTCHA v2/v3
 * - Comunicación con API (/api/login)
 * - Redirección automática a dashboard
 * 
 * Args:
 *   recaptchaResponse (string): Token generado por widget reCAPTCHA
 * 
 * Raises:
 *   Error: Si reCAPTCHA no está cargado o respuesta es inválida
 *   Error: Si API retorna success=false
 * 
 * Ejemplo:
 *   // Flujo de autenticación exitoso
 *   grecaptcha.execute();
 *   fetch("/api/login", {
 *     method: "POST",
 *     body: JSON.stringify({ nombre: "admin", password: "admin", recaptcha: "token" })
 *   });
 */
// Espera a que el contenido del DOM se cargue por completo
document.addEventListener("DOMContentLoaded", function() {
    // Se obtiene los campos de la pagina
    const loginBtn = document.getElementById("loginBtn");
    const nameInput = document.getElementById("name");
    const passworInput = document.getElementById("password");
    const recaptchaError = document.getElementById("recaptchaError");

    // Se valida la existencia de los campos
    if (!loginBtn || !nameInput || !passworInput || !recaptchaError) {
        console.error("Elementos requeridos no fueron encontrados en el DOM")
        return;
    }

    loginBtn.addEventListener("click", function() {
        // Se obtienen los valores de los campos
        const name = nameInput.value.trim();
        const password = passworInput.value.trim();

        // Valida campos vacíos
        if (!name && !password) {
            alert("Por favor, ingresa tu nombre de usuario y contraseña");
            return;
        }

        if (!name) {
            alert("Por favor, ingresa tu nombre de usuario");
            return;
        }

        if (!password) {
            alert("Por favor, ingresa contraseña");
            return;
        }

        // Valida que exista el reCAPTCHA
        if (typeof grecaptcha === "undefined") {
            console.error("reCAPTCHA not loaded")
            alert("Error de seguridad. Por favor, recarga la página.")
            return;
        }

        // Valida la respuesta del reCAPTCHA
        const recaptchaResponse = grecaptcha.getResponse();

        if (!recaptchaResponse) {
            recaptchaError.textcontent = "por favor, completa el recaptcha";
            recaptchaError.style.display = "block";
            return;
        }

        recaptchaError.style.display = "none";

        // Validar si los datos son validos para entrar
        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                nombre: name,
                password: password,
                recaptcha: recaptchaResponse,
            }),
        }).then(response => response.json()).then(data => {
            if (data.success) {
                // Redirectionar si se pudo hacer el login
                window.location.href = `/dashboard?timestamp=${Date.now()}`;
            } else {
                // Mostrar error si sucede
                alert(data.message || "Error al iniciar sesión");
            }
        }).catch(error => {
            // Mostrar error si sucede
            console.error("Error:", error);
            alert('Ocurrio un error al iniciar sesión');
        }).finally(() => {
            // Limpiar formulario después del login
            document.getElementById("name").value = "";
            document.getElementById("password").value = "";
            grecaptcha.reset();
        });
    });
});
