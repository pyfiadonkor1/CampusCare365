// Get all the table cells in the tbody
const cells = document.querySelectorAll("tbody td");

// Add a click event listener to each cell
cells.forEach((cell) => {
  cell.addEventListener("click", function () {
    // Get the current meal name or prompt the user to enter a new one
    let mealName = this.textContent.trim();
    if (!mealName) {
      mealName = prompt("Enter meal name:");
      if (!mealName) {
        return;
      }
    }

    // Display options to edit or delete the meal
    const action = prompt("Options:\n1. Edit\n2. Delete");
    if (!action) {
      return;
    }

    // Perform the selected action
    if (action === "1") {
      // Edit the meal name
      const newMealName = prompt("Enter new meal name:", mealName);
      if (newMealName) {
        this.textContent = newMealName;
      }
    } else if (action === "2") {
      // Delete the meal name
      this.textContent = "+";
    }

})

});