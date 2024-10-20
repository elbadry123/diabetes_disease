// script.js

document.getElementById('predictionForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const formDataObj = {};
    formData.forEach((value, key) => formDataObj[key] = value);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataObj)
        });

        const result = await response.json();
        document.getElementById('result').textContent = result.prediction === 1 ? 'Diabetes Detected' : 'No Diabetes Detected';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Error in prediction';
    }
});
