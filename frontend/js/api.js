// js/api.js
//
// Este archivo define las funciones para interactuar con el backend de Django.
// Aquí centralizamos el uso de fetch, incluyendo los headers necesarios,
// manejo de autenticación y errores básicos.

// === Configuración base de la API ===

// URL base del backend. Ajusta si usas un dominio diferente.
const API_BASE_URL = "http://localhost:8000/api";

console.clear()
console.log(getAccessToken())

// Recupera el token de sesión (si existe).
function getAccessToken() {
    return sessionStorage.getItem("access");
}

// Recupera el refresh token.
function getRefreshToken() {
    return sessionStorage.getItem("refresh");
}

// Guarda el token de sesión.
function setAccessToken(token) {
    sessionStorage.setItem("access", token);
}

// Guarda el refresh
function setRefreshToken(token) {
    sessionStorage.setItem("refresh", token);
}

// Borra el token (logout).
function clearAccessToken() {
    sessionStorage.removeItem("access");
    sessionStorage.removeItem("refresh")
}


// async function refreshAccessToken() {
//     const refreshToken = getRefreshToken();
//     if (!refreshToken) {
//         throw new Error("No hay refresh token disponible");
//     }

//     const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ refresh: refreshToken }),
//     });

//     if (!response.ok) {
//         throw new Error("No se pudo refrescar el token");
//     }

//     const data = await response.json();
//     setAccessToken(data.access); // guardamos el nuevo access token
//     return data.access;
// }


// === Función principal para hacer requests ===
/**
 * fetchWithAuth
 * Envuelve fetch() para incluir automáticamente el header Authorization
 * si hay un token guardado en sessionStorage.
 *
 * @param {string} endpoint - Ruta relativa del endpoint (ej: "/users/")
 * @param {object} options - Opciones de fetch (method, headers, body)
 * @returns {Promise} - Respuesta en JSON o error
 */
async function fetchWithAuth(endpoint, options = {}) {
    let token = getAccessToken();

    // Construir headers
    let headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        let response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        // Si el servidor responde con 204 (No Content)
        if (response.status === 204) {
            return null;
        }

        // Si el token expiró (401)
        if (response.status === 401) {
            try {
                // Intentamos refrescar
                const newAccessToken = await refreshAccessToken();

                // Reintentar la petición con el nuevo token
                headers["Authorization"] = `Bearer ${newAccessToken}`;
                response = await fetch(`${API_BASE_URL}${endpoint}`, {
                    ...options,
                    headers,
                });

                if (response.status === 204) return null;
            } catch (refreshError) {
                console.error("Error refrescando token:", refreshError);
                clearAccessToken(); // opcional: limpiar también el refresh
                window.location.href = "index.html"; // forzar login
                throw refreshError;
            }
        }

        // Intentar parsear respuesta JSON
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Error en la petición");
        }

        return data;
    } catch (error) {
        console.error("Error en fetchWithAuth:", error);
        throw error;
    }
}
