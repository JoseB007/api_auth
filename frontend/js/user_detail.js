function getUserIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id"); // devuelve "3" (string)
}


document.addEventListener("DOMContentLoaded", async () => {
    const userId = getUserIdFromUrl();
    if (!userId) {
        console.error("No se encontró el id del usuario en la URL");
        return;
    }
    
    try {
        // Petición al endpoint detalle
        const user = await fetchWithAuth(`/usuarios/${userId}/`);
        console.log("Detalle del usuario:", user);
    
        // Mostrar en el HTML
        document.getElementById("userId").textContent = user.id;
        document.getElementById("username").textContent = user.username;
        document.getElementById("email").textContent = user.email;
        document.getElementById("firstName").textContent = user.first_name;
        document.getElementById("lastName").textContent = user.last_name;
    } catch (error) {
        console.error("Error cargando usuario:", error);
    }
})