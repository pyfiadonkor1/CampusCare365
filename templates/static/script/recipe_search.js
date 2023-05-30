document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.getElementById('query').value;
    const cuisine = document.getElementById('cuisine').value;
    const diet = document.getElementById('diet').value;
    const intolerances = document.getElementById('intolerances').value;
    const excludeIngredients = document.getElementById('excludeIngredients').value;
    const type = document.getElementById('type').value;
    const instructionsRequired = document.getElementById('instructionsRequired').checked;
    const fillIngredients = document.getElementById('fillIngredients').checked;
    const addRecipeNutrition = document.getElementById('addRecipeNutrition').checked;
    const apiKey = 'bb96fafd19b64b4c86b0f79c917cd7fe'; 

    let searchUrl = `https://api.spoonacular.com/recipes/complexSearch?apiKey=${apiKey}&type=${type}&instructionsRequired=${instructionsRequired}&fillIngredients=${fillIngredients}&addRecipeNutrition=${addRecipeNutrition}`;

    if (query) {
        searchUrl += `&query=${query}`;
    }
    if (cuisine) {
        searchUrl += `&cuisine=${cuisine}`;
    }
    if (diet) {
        searchUrl += `&diet=${diet}`;
    }
    if (intolerances) {
        searchUrl+= `&intolerances=${intolerances}`;
    }
    if (excludeIngredients) {
        searchUrl += `&excludeIngredients=${excludeIngredients}`;
    }

    fetch(searchUrl)
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('results');
            results.innerHTML = '';
            data.results.forEach(recipe => {
                const recipeDiv = document.createElement('div');
                recipeDiv.className = 'card mb-4';
                recipeDiv.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${recipe.title}</h5>
                    <p class="card-text">Ready in ${recipe.readyInMinutes} minutes</p>
                    <a href="${recipe.sourceUrl}" class="btn btn-primary" target="_blank">View Recipe</a>
                </div>
                `;
                results.appendChild(recipeDiv);
            });
        })
        .catch(error => console.error(error));
});