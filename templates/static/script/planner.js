// Sample to-do list data
let todoList = [
{title: "Buy groceries", date: "2023-05-14", time: "10:00", completed: false},
{title: "Do laundry", date: "2023-05-15", time: "12:00", completed: false},
{title: "Pay bills", date: "2023-05-16", time: "14:00", completed: false},
{title: "Finish project", date: "2023-05-17", time: "16:00", completed: false},
{title: "Call mom", date: "2023-05-18", time: "18:00", completed: false},
];

// Get DOM elements
const loader = document.querySelector(".loader .loading-bar");
const todoListContainer = document.querySelector(".todo-list");
const addTodoForm = document.querySelector(".add-todo form");

// Load the to-do list items
loadTodoList();

// Add event listener to the add todo form
addTodoForm.addEventListener("submit", function(event) {
event.preventDefault();
const title = event.target.elements.title.value;
const date = event.target.elements.date.value;
const time = event.target.elements.time.value;

// Validate date and time
const dateTime = new Date(`${date} ${time}`);
if (isNaN(dateTime.getTime())) {
    alert("Please enter a valid date and time.");
    return;
}

// Add the new todo item to the list and reset the form
todoList.push({title, date, time, completed: false});
addTodoForm.reset();
loadTodoList();
});

// Function to load the to-do list items
function loadTodoList() {
// Clear the todo list container
todoListContainer.innerHTML = "";

// Add each todo item to the container
todoList.forEach(function(item, index) {
    const todoItem = document.createElement("div");
    todoItem.classList.add("todo-item");
    if (item.completed) {
    todoItem.classList.add("completed");
    }

    const title = document.createElement("h3");
    title.textContent = item.title;
    todoItem.appendChild(title);

    const dateTime = new Date(`${item.date} ${item.time}`);
    const date = document.createElement("p");
    date.textContent = dateTime.toLocaleDateString();
    todoItem.appendChild(date);

    const time = document.createElement("p");
    time.textContent = dateTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    todoItem.appendChild(time);

    const deleteButton = document.createElement("span");
    deleteButton.classList.add("delete");
    deleteButton.textContent = "×";
    deleteButton.addEventListener("click", function() {
    todoList.splice(index, 1);
    loadTodoList();
    });
    todoItem.appendChild(deleteButton);

    const editButton = document.createElement("span");
    editButton.classList.add("edit");
    editButton.textContent = "✎";
    editButton.addEventListener("click", function() {
    const newTitle = prompt("Enter new title:", item.title);
    if (newTitle !== null) {
        item.title = newTitle;
        loadTodoList();
    }
    });
    todoItem.appendChild(editButton);

    editButton.addEventListener("click", function() {
        const newTitle = prompt("Enter new title:", item.title);
        if (newTitle !== null) {
          const newDate = prompt("Enter new date (YYYY-MM-DD):", item.date);
          const newTime = prompt("Enter new time (HH:MM):", item.time);
          // Validate date and time
          const dateTime = new Date(`${newDate} ${newTime}`);
          if (isNaN(dateTime.getTime())) {
            alert("Please enter a valid date and time.");
            return;
          }
          item.title = newTitle;
          item.date = newDate;
          item.time = newTime;
          loadTodoList();
        }
      });

    todoItem.addEventListener("click", function() {
    item.completed = !item.completed;
    loadTodoList();
    });

    todoListContainer.appendChild(todoItem);
});

// Update the loader
const completedItems = todoList.filter(item => item.completed).length;
const percentCompleted = (completedItems / todoList.length) * 100;
loader.style.width = `${percentCompleted}%`;
}