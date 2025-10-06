// Lógica para la pantalla de usuarios (users.html).
// Carga la lista de usuarios desde el backend y los muestra en la página.
const USERS_URL = "/usuarios/";

document.addEventListener("DOMContentLoaded", async () => {
    // Verificar que el usuario esté autenticado
    requireAuth();

    const token = getAccessToken();
    const usersTableBody = document.getElementById("usersTableBody");
    const logoutBtn = document.getElementById("logout");
    const userDiv = document.getElementById("user");

    // Evento de logout
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    }

    try {
        // Hacer petición al backend
        const response = await fetchWithAuth(`${USERS_URL}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        // Limpiar el contenido previo por si se recarga la lista
        usersTableBody.innerHTML = "";

        // Iterar sobre los usuarios
        response.forEach((user) => {
            // Crear una fila
            const tr = document.createElement("tr");

            // Crear y llenar celdas (td) para cada columna
            const tdId = document.createElement("td");
            tdId.textContent = user.id;

            const tdUsername = document.createElement("td");
            tdUsername.textContent = user.username;
            tdUsername.style.cursor = "pointer";

            const tdEmail = document.createElement("td");
            tdEmail.textContent = user.email;

            const tdFirstName = document.createElement("td");
            tdFirstName.textContent = user.first_name;

            const tdLastName = document.createElement("td");
            tdLastName.textContent = user.last_name;

            // Agregar un evento de clic SOLO al username (para redirigir)
            tdUsername.addEventListener("click", () => {
                window.location.href = `user_detail.html?id=${user.id}`;
            });

            // Insertar las celdas en la fila
            tr.appendChild(tdId);
            tr.appendChild(tdUsername);
            tr.appendChild(tdEmail);
            tr.appendChild(tdFirstName);
            tr.appendChild(tdLastName);

            // Insertar la fila en la tabla
            usersTableBody.appendChild(tr);
        });
    } catch (error) {
        console.error("Error en fetchWithAuth:", error);
        throw error;
    }
});
