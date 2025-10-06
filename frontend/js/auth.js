// Lógica de autenticación: login, logout y validación de sesión.
// Este archivo se carga en index.html (login) y lo podemos reutilizar en otras páginas
// para verificar si el usuario está autenticado.

// URL de login y logout
const LOGIN_URL = "/token/";
const LOGOUT_URL = "/logout/";

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

        // Guardar el token de acceso en sessionStorage
        setAccessToken(data.access);
        setRefreshToken(data.refresh);

        // Redirigir a la lista de usuarios
        window.location.href = "users.html";
    } catch (error) {
        const messageDiv = document.getElementById("message");
        if (messageDiv) {
            messageDiv.textContent = error.message;
        }
    }
}

// === LOGOUT ===
function logout() {
    try {
        const response = fetchWithAuth(`${LOGOUT_URL}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${getAccessToken()}`,
            },
            body: JSON.stringify({"refresh": getRefreshToken()}),
        });
    
        if (!response.ok) {
            throw new Error("No se pudo cerrar la sesión");
        } 

        // Borrar el token
        clearAccessToken();

        // Redirigir al login
        window.location.href = "index.html";
    } catch(error) {
        const messageDiv = document.getElementById("message");
        if (messageDiv) {
            messageDiv.textContent = error.message;
        }
    }

}

// Si no hay token → redirigir al login
function requireAuth() {
    const token = getAccessToken();
    if (!token) {
        window.location.href = "index.html";
    }
}

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