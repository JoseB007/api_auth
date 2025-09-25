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