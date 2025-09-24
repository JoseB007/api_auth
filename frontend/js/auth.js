// js/auth.js
//
// Lógica de autenticación: login, logout y validación de sesión.
// Este archivo se carga en index.html (login) y lo podemos reutilizar en otras páginas
// para verificar si el usuario está autenticado.

//
// === LOGIN ===
//

// URL de login (ajusta si tu endpoint es distinto, por ejemplo /token/ o /auth/jwt/create/)
const LOGIN_URL = "/token/";

// Función para hacer login
async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}${LOGIN_URL}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Credenciales inválidas");
        }

        console.log(data)

        // Guardar el token de acceso en sessionStorage
        // setAccessToken(data.access);

        // (Si tu backend también devuelve refresh, lo guardamos después)
        // sessionStorage.setItem("refresh", data.refresh);

        // Redirigir a la lista de usuarios
        // window.location.href = "users.html";
    } catch (error) {
        const messageDiv = document.getElementById("message");
        if (messageDiv) {
            messageDiv.textContent = error.message;
        }
    }
}

//
// === LOGOUT ===
//
function logout() {
    clearAccessToken();
    window.location.href = "index.html";
}

//
// === PROTECCIÓN DE PÁGINAS ===
//

// Si no hay token → redirigir al login
function requireAuth() {
    const token = getAccessToken();
    if (!token) {
        window.location.href = "index.html";
    }
}

//
// === EVENTOS DEL LOGIN ===
//

// Solo se ejecuta en index.html
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    if (form) {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            login(username, password);
        });
    }
});
