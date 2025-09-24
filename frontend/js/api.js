// js/api.js
//
// Este archivo define las funciones para interactuar con el backend de Django.
// Aquí centralizamos el uso de fetch, incluyendo los headers necesarios,
// manejo de autenticación y errores básicos.

// === Configuración base de la API ===

// URL base del backend. Ajusta si usas un dominio diferente.
const API_BASE_URL = "http://localhost:8000/api";

// Recupera el token de sesión (si existe).
function getAccessToken() {
    return sessionStorage.getItem("access");
}

// Guarda el token de sesión.
function setAccessToken(token) {
    sessionStorage.setItem("access", token);
}

// Borra el token (logout).
function clearAccessToken() {
    sessionStorage.removeItem("access");
}

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
    const token = getAccessToken();

    // Construir headers
    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        // Si el servidor responde con 204 (No Content)
        if (response.status === 204) {
            return null;
        }

        // Intentar parsear respuesta JSON
        const data = await response.json();

        if (!response.ok) {
            // Si la respuesta es un error (4xx, 5xx)
            throw new Error(data.detail || "Error en la petición");
        }

        return data;
    } catch (error) {
        console.error("Error en fetchWithAuth:", error);
        throw error;
    }
}
