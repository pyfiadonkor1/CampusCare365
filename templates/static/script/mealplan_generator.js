
const apiKey = 'bb96fafd19b64b4c86b0f79c917cd7fe';

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
    success: function(data) {
      let html = '<table>';
      for (const day in data.week) {
        const meals = data.week[day].meals;
        const nutrients = data.week[day].nutrients;
    
        html += `<tr><th colspan="6">${day.charAt(0).toUpperCase() + day.slice(1)}</th></tr>`;
        html += '<tr><th>Title</th><th>Ready in minutes</th><th>Servings</th><th>Calories</th><th>Protein</th><th>Fat</th><th>Carbohydrates</th></tr>';
        meals.forEach(meal => {
          const mealNutrients = meal.nutrition && meal.nutrition.nutrients ? meal.nutrition.nutrients : { calories: '', protein: '', fat: '', carbohydrates: '' };
          html += `<tr><td><a href="${meal.sourceUrl}" target="_blank">${meal.title}</a></td><td>${meal.readyInMinutes}</td><td>${meal.servings}</td><td>${mealNutrients.calories ? Math.round(mealNutrients.calories) : ''}</td><td>${mealNutrients.protein ? Math.round(mealNutrients.protein) : ''}</td><td>${mealNutrients.fat ? Math.round(mealNutrients.fat) : ''}</td><td>${mealNutrients.carbohydrates ? Math.round(mealNutrients.carbohydrates) : ''}</td></tr>`;
        });
        html += `<tr><td colspan="3"><b>Total</b></td><td>${Math.round(nutrients.calories)}</td><td>${Math.round(nutrients.protein)}</td><td>${Math.round(nutrients.fat)}</td><td>${Math.round(nutrients.carbohydrates)}</td></tr>`;
      }
      html += '</table>';
    
      // Create a new window and write the HTML to it
      const newWindow = window.open('', '_blank');
      newWindow.document.write(html);
    },
    error: function (error) {
      console.error('Error:', error);
    }
  });
});
