

const apiKey = 'bb96fafd19b64b4c86b0f79c917cd7fe';

$(document).ready(function () {
   
    const diets = [
        'Gluten Free', 'Ketogenic', 'Vegetarian', 'Lacto-Vegetarian', 'Ovo-Vegetarian',
        'Vegan', 'Pescetarian', 'Paleo', 'Primal', 'Low FODMAP', 'Whole30'
    ];
    diets.forEach(diet => {
        $('#diet').append(`<option value="${diet}">${diet}</option>`);
    });

    //Submission Handler
    $('#meal-planner-form').on('submit', function (e) {
        e.preventDefault();

        const timeFrame = $('#timeFrame').val();
        const targetCalories = $('#targetCalories').val();
        const diet = $('#diet').val();
        const exclude = $('#exclude').val();

        // Query the Spoonacular API
        $.ajax({
            url: `https://api.spoonacular.com/mealplanner/generate?apiKey=${apiKey}&timeFrame=${timeFrame}&targetCalories=${targetCalories}&diet=${diet}&exclude=${exclude}`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Set table body reference
                const tableBody = $('#meal-plan-result');
                tableBody.empty();
              
                if (data.week) {
                  const weekDays = Object.keys(data.week);
              
                  weekDays.forEach(day => {
                    const meals = data.week[day].meals;
                    meals.forEach(meal => {
                      tableBody.append(`
                        <tr>
                          <td>${day}</td>
                          <td>${meal.title}</td>
                          <td>${meal.readyInMinutes} min</td>
                          <td>${meal.nutrients.calories.toFixed(0)} kcal</td>
                          <td><a href="${meal.sourceUrl}" target="_blank">View Recipe</a></td>
                        </tr>
                      `);
                    });
                  });
                } else if (data.day) {
                  const meals = data.day.meals;
              
                  meals.forEach((meal, index) => {
                    tableBody.append(`
                      <tr>
                        <td>Meal ${index + 1}</td>
                        <td>${meal.title}</td>
                        <td>${meal.readyInMinutes} min</td>
                        <td>${meal.nutrients.calories.toFixed(0)} kcal</td>
                        <td><a href="${meal.sourceUrl}" target="_blank">View Recipe</a></td>
                      </tr>
                    `);
                  });
                } else {
                  tableBody.append('<tr><td colspan="5">No meal plan found.</td></tr>');
                }
              },
        
        });
    });
});
