// js/users.js
//
// Lógica para la pantalla de usuarios (users.html).
// Carga la lista de usuarios desde el backend y los muestra en la página.
const USERS_URL = "/usuarios/";

document.addEventListener("DOMContentLoaded", async () => {
    // Verificar que el usuario esté autenticado
    requireAuth();

    const token = getAccessToken();
    const usersList = document.getElementById("users-list");
    const logoutBtn = document.getElementById("logout-btn");

    // Evento de logout
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    }

    try {
        // Hacer petición al backend
        const response = await fetchWithAuth(`${API_BASE_URL}${USERS_URL}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        console.log(response)

        // Renderizar usuarios en la lista
        // usersList.innerHTML = ""; // Limpiar contenido previo
        // data.forEach((user) => {
        //     const li = document.createElement("li");
        //     li.textContent = `${user.id} - ${user.username}`;
        //     li.style.cursor = "pointer";

        //     // Al hacer clic, redirige al detalle
        //     li.addEventListener("click", () => {
        //         window.location.href = `user_detail.html?id=${user.id}`;
        //     });

        //     usersList.appendChild(li);
        // });
    } catch (error) {
        usersList.innerHTML = `<li>${error.message}</li>`;
    }
});
