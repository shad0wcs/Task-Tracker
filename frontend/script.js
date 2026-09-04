async function login(email, password) {
    const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
    });

    if (!response.ok) {
        alert('Неверный Email или Пароль')
        return;
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    window.location.href = "tasks.html";
}

document.querySelector("form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.querySelector('input[type="email"]').value;
    const password = document.querySelector('input[type="password"]').value;

    await login(email, password);
});