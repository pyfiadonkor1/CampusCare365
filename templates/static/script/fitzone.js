//I will return to implement this section

function calculateBMI() {
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;
    const weightUnit = document.getElementById("weight-unit").value;
    const heightUnit = document.getElementById("height-unit").value;
    
    let url = "";
    let querystring = {};
    
    if (weightUnit === "kg" && heightUnit === "m") {
      url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/metric";
      querystring = {"weight": weight, "height": height};
    } else if (weightUnit === "lb" && heightUnit === "in") {
      url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/imperial";
      querystring = {"weight": weight, "height": height};
    } else {
      alert("Invalid unit combination. Please select kg/m or lb/in.");
      return;
    }
    
    const headers = {
      "X-RapidAPI-Key": "395bbed80emshbb95db48e059abcp179b15jsn9adb18754dba",
      "X-RapidAPI-Host": "body-mass-index-bmi-calculator.p.rapidapi.com"
    };
    
    fetch(url + "?" + new URLSearchParams(querystring), {headers})
    .then(response => response.json())
    .then(data => {
      const bmi =data.bmi;
        let category = '';
        if (bmi < 18.5) {
        category = 'Underweight';
        } else if (bmi >= 18.5 && bmi < 25) {
        category = 'Normal weight';
        } else if (bmi >= 25 && bmi < 30) {
        category = 'Overweight';
        } else if (bmi >= 30) {
        category = 'Obese';
        }
      //const category = data.bmiCategory;
      const resultElement = document.getElementById("bmi");
     
      resultElement.innerHTML = `Your BMI is ${bmi.toFixed(1)}, which is ${category}.`;
    })
    .catch(error => {
      console.error(error);
      alert("An error occurred while calculating your BMI. Please try again later.");
    });
  }

const collapsible = document.querySelector(".collapsible");
const content = document.querySelector(".content");

collapsible.addEventListener("click", function() {
content.classList.toggle("active");
if (content.style.maxHeight) {
    content.style.maxHeight = null;
} else {
    content.style.maxHeight = content.scrollHeight + "px";
}
});

