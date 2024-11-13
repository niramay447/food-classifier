import { Client } from "@gradio/client";

// Initialize client connection
async function classifyImage() {
    const imageInput = document.getElementById("imageInput").files[0];
    const resultDiv = document.getElementById("result");
    
    if (!imageInput) {
        resultDiv.textContent = "Please upload an image.";
        return;
    }

    resultDiv.textContent = "Classifying...";

    try {
        // Read the uploaded image as a blob
        const imageBlob = await imageInput.arrayBuffer();
        
        const client = await Client.connect("niramay/food"); // Replace with actual Space ID
        const result = await client.predict("/predict", { img: new Blob([imageBlob]) });

        const label = result.data.label;
        const probabilities = result.data.probabilities;

        // Display result
        resultDiv.innerHTML = `<strong>Prediction:</strong> ${label}<br>`;

        // If probabilities are returned, display them
        if (probabilities) {
            resultDiv.innerHTML += `<strong>Probabilities:</strong><br>`;
            for (const [foodType, probability] of Object.entries(probabilities)) {
                resultDiv.innerHTML += `${foodType}: ${(probability * 100).toFixed(2)}%<br>`;
            }
        }
    } catch (error) {
        console.error(error);
        resultDiv.textContent = "Error occurred while classifying the image.";
    }
}