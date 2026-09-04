async function loadTasks() {
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/tasks", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const tasks = await response.json();

    const taskList = document.querySelector("#task-list");
    tasks.forEach(function(task) {
        const li = document.createElement("li");
        li.textContent = task.title;
        taskList.appendChild(li);
    });
}

loadTasks();