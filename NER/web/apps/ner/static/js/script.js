document.addEventListener('DOMContentLoaded', function() {
    // Extract the AUTH_TOKEN from the URL hash
    const token = window.location.hash.substring(1); // Remove '#' from the beginning
    // Populate the token into the form field
    const tokenField = document.getElementById('tokenField');
    const checkButton = this.getElementById('checkTokenButton');
    const processButton = this.getElementById('processButton');
    
    // Populate the token into the form field and adjust field properties if token exists
    if (token) {
        tokenField.value = token;
        checkTokenValidity(token).then(isValid => {
            if (isValid) {
                tokenField.disabled = true; // Disable the field
                checkButton.disabled = true; // Disable the field
                tokenField.classList.add('is-valid');
                processButton.classList.replace('btn-outline-secondary', 'btn-outline-dark');
                processButton.disabled = false;
                console.log('Token is valid.');
            } else {
                tokenField.classList.add('is-invalid');
                processButton.disabled = true;
                console.log('Token is invalid.');
            }
        });
    }

    checkTokenButton.addEventListener('click', function() {
        // Get the current value of the token input field
        const token = document.getElementById('tokenField').value;
        // Call the checkTokenValidity function with the token
        checkTokenValidity(token).then(isValid => {
            if (isValid) {
                tokenField.classList.replace('is-invalid', 'is-valid');
                processButton.classList.replace('btn-outline-secondary', 'btn-outline-dark');
                processButton.disabled = false;
                console.log('Token is valid.');
            } else {
                tokenField.classList.replace('is-valid', 'is-invalid');
                processButton.disabled = true;
                console.log('Token is invalid.');
            }
        });
    });

    
});

async function checkTokenValidity(token) {
    // Define the URL for the API endpoint
    const url = '/api/auth/validate_token';

    // Prepare the request body
    const requestBody = {
        token: token
    };

    try {
        // Send a POST request to the API endpoint
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        // Check if the request was successful
        if (!response.ok) {
            console.error('Error validating token:', response.statusText);
            return false; // Return false if the request failed
        }

        // Parse the JSON response
        const data = await response.json();

        if (data.status === 'valid') {
            return true; // Return true if the token is valid
        } else {
            return false; // Return false if the token is invalid
        }
    } catch (error) {
        console.error('Error:', error);
        return false; // Return false in case of any error
    }
}

async function processAndDisplay() {
    // Get the text from the input field
    const text = document.getElementById('textInput').value;
    const token = document.getElementById('tokenField').value;
    const processButton = document.getElementById('loadingIndicator');

    processButton.classList.remove("invisible");

    // Ensure the token is present
    if (!token) {
        console.error('Token is missing.');
        return;
    }

    // Send a request to the FastAPI endpoint
    const response = await fetch('/api/ner/process-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // Use the token from the form
        },
        body: JSON.stringify({ text: text }),
    });

    // Check if the request was successful
    if (!response.ok) {
        console.error('Error processing text:', response.statusText);
        return;
    }

    // Parse the JSON response
    const matches = await response.json();

   /*OLD
   // Get the text and matches JSON from the input fields
    const text = document.getElementById('textInput').value;
    const matchesJson = document.getElementById('matchesInput').value;

    // Parse the JSON string into a JavaScript object
    const matches = JSON.parse(matchesJson);
    */
  
  
    // Function to process the text and generate HTML
    function processText(text, matches) {
        let processedText = text;
        let colorIndex = 1; // Initialize color index
        // TODO: Write a heuristic for overlap, maybe longest match first
        for (const category in matches) {
            matches[category].forEach(item => {
                const regex = new RegExp(item, 'g'); //gi for non case sensitive
                processedText = processedText.replace(regex, match => {
                    // Create a span element
                    const span = document.createElement('span');
                    span.className = 'match';
                    span.style.backgroundColor = `var(--color-${colorIndex})`;
                    span.dataset.category = category;
                    span.textContent = match;

                    // Create an action span element
                    const actionSpan = document.createElement('span');
                    actionSpan.className = 'action';
                    actionSpan.textContent = '🐞';

                    // Append the action span to the match span
                    span.appendChild(actionSpan);

                    // Convert the span to an HTML string
                    return span.outerHTML;
                });
            });
            colorIndex++; // Increment color index for the next category
        }
        return processedText;
    }

    // Process the text and generate the HTML
    const html = processText(text, matches);

    // Display the result
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = html;

    // Attach event listeners to the newly created .match elements
    resultDiv.querySelectorAll('.match').forEach(function(matchSpan) {
        matchSpan.addEventListener('mouseover', function() {
            this.classList.add('hovered');
        });
        matchSpan.addEventListener('mouseout', function() {
            this.classList.remove('hovered');
        });
    });


    function generateJsonOutput(matches) {
        let outputHtml = '';
        let colorIndex = 1; // Initialize color index

        for (const category in matches) {
            outputHtml += `<b>${category}</b>`;
            outputHtml += '<div class="match-list">';
            matches[category].forEach(item => {
                outputHtml += `<div class="match" style="background-color: var(--color-${colorIndex});">${item}</div>`;
            });
            outputHtml += '</div>';
            colorIndex++; // Increment color index for the next category
        }

        // Display the JSON output in a new section of the HTML
        const jsonOutputDiv = document.getElementById('jsonOutput');
        jsonOutputDiv.innerHTML = outputHtml;
    }

    // Call the new function to generate and display the JSON output
    generateJsonOutput(matches);

    // Hide loading indicator
    processButton.classList.add("invisible");

}