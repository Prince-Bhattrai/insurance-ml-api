
document.addEventListener('DOMContentLoaded', () => {
    
    const inputs = document.querySelectorAll('.input-box input');
    inputs.forEach(input => {
        input.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendData();
            }
        });
    });
});

async function sendData() {
    const resultElement = document.getElementById('result');
    resultElement.textContent = 'Predicting...'; 
    resultElement.style.color = 'blue';

    const age = document.getElementById('age').value;
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;
    const income = document.getElementById('income').value;
    const smokerInput = document.getElementById('smoker').value.toLowerCase().trim();
    const city = document.getElementById('city').value.trim();
    const occupationInput = document.getElementById('occupation').value.toLowerCase().trim(); 

    if (!age || !weight || !height || !income || !smokerInput || !city || !occupationInput) {
        resultElement.textContent = 'Please fill in all fields.';
        resultElement.style.color = 'red';
        return; 
    }

    let isSmokerBoolean;
    if (smokerInput === 'yes') {
        isSmokerBoolean = true;
    } else if (smokerInput === 'no') {
        isSmokerBoolean = false;
    } else {
        resultElement.textContent = 'For "Do you smoke?", please enter "yes" or "no".';
        resultElement.style.color = 'red';
        return; 
    }

    const validOccupations = [
        'retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed', 'private_job'
    ];

    if (!validOccupations.includes(occupationInput)) {
        resultElement.textContent = `Invalid occupation. Please choose from: ${validOccupations.join(', ')}.`;
        resultElement.style.color = 'red';
        return; 
    }

    const data = {
        age: parseInt(age),
        weight: parseFloat(weight),
        height: parseFloat(height),
        income_lpa: parseFloat(income),
        smoker: isSmokerBoolean,
        city: city,
        occupation: occupationInput
    };

    const apiUrl = 'http://localhost:8000/predict';

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            resultElement.textContent = `Predicted Category: ${result.predicted_category}`;
            resultElement.style.color = 'green';
        } else {
            const errorData = await response.json(); 
            resultElement.textContent = `Error: ${response.status} - ${JSON.stringify(errorData.detail || errorData)}`;
            resultElement.style.color = 'red';
            console.error('API Error:', errorData); 
        }
    } catch (error) {
        resultElement.textContent = `Network Error: ${error.message}. Make sure the backend is running and accessible at ${apiUrl}.`;
        resultElement.style.color = 'red';
        console.error('Fetch Error:', error);
    }
}
