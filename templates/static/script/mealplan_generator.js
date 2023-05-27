

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
                // Display the meal plan result
                $('#meal-plan-result').html(`<pre>${JSON.stringify(data, null, 2)}</pre>`);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});
