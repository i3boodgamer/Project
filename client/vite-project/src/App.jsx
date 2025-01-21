import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Подключаем стили

function App() {
  const [tasks, setTasks] = useState([]);
  const [newDescription, setNewDescription] = useState("");
  const [newTitle, setNewTitle] = useState("");

  // Загрузка задач с бэкенда
  useEffect(() => {
    axios
      .get("http://localhost:8000/tasks")  // URL вашего FastAPI сервера
      .then((response) => {
        setTasks(response.data);  // Устанавливаем данные в состояние
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });
  }, []);

  // Добавление новой задачи
  const addTask = () => {
    const task = {
      description: newDescription,  // Используем description
      title: newTitle,  // Используем title вместо done
    };

    axios
      .post("http://localhost:8000/tasks", task)
      .then((response) => {
        setTasks([...tasks, response.data]);  // Добавляем новую задачу в список
        setNewDescription("");  // Очистить поле ввода description
        setNewTitle("");  // Очистить поле ввода title
      })
      .catch((error) => {
        console.error("Error adding task:", error);
      });
  };

  return (
    <div className="app-container">
      <h1>Task Manager</h1>
      <div className="input-container">
        <input
          type="text"
          value={newDescription}
          onChange={(e) => setNewDescription(e.target.value)}
          placeholder="Task description"
        />
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Task title"
        />
        <button onClick={addTask}>Add Task</button>
      </div>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong>: {task.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
