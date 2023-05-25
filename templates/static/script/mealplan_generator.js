
const dietPlanForm = document.getElementById('dietPlanForm');
const resultDiv = document.getElementById('result');

dietPlanForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;
    const allergies = document.getElementById('allergies').value;
    const unliked_foods = document.getElementById('unliked_foods').value;

    const apiUrl = "https://customized-meal-plan-generator.p.rapidapi.com/diet_plan";
    const apiKey = "395bbed80emshbb95db48e059abcp179b15jsn9adb18754dba";

    const headers = new Headers({
        "X-RapidAPI-Key": apiKey,
        "X-RapidAPI-Host": "customized-meal-plan-generator.p.rapidapi.com"
    });

    const queryParams = new URLSearchParams({
        height,
        weight,
        allergies,
        unliked_foods
    });

    const response = await fetch(`${apiUrl}?${queryParams}`, { headers });
    const data = await response.json();

    resultDiv.innerHTML = JSON.stringify(data, null, 2);
});
