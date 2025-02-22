// Replace these endpoints with your actual backend routes that call ChatGPT and DALL·E
const CHATGPT_API_URL = "/api/chatgpt"; // Example endpoint
const DALLE_API_URL = "/api/dalle";     // Example endpoint

// Grab elements from the DOM
const dreamForm = document.getElementById("dreamForm");
const analysisOutput = document.getElementById("analysisOutput");
const dreamImage = document.getElementById("dreamImage");
const tweakInput = document.getElementById("tweakInput");
const tweakBtn = document.getElementById("tweakBtn");

// Handle form submit
dreamForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Collect form data
  const theme = document.getElementById("theme").value.trim();
  const characters = document.getElementById("characters").value.trim();
  const events = document.getElementById("events").value.trim();

  // Step 1: Send the dream details to ChatGPT
  let dreamAnalysis, dallePrompt;
  try {
    const response = await fetch(CHATGPT_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ theme, characters, events }),
    });

    const data = await response.json();
    dreamAnalysis = data.analysis;
    dallePrompt = data.prompt;     // The prompt to pass to DALL·E
  } catch (error) {
    console.error("Error calling ChatGPT API:", error);
    analysisOutput.innerText = "An error occurred while interpreting your dream.";
    return;
  }

  // Display dream analysis
  analysisOutput.innerText = dreamAnalysis || "No analysis returned.";

  // Step 2: Generate an image with DALL·E
  try {
    const imageResponse = await fetch(DALLE_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: dallePrompt })
    });
    const imageData = await imageResponse.json();

    if (imageData && imageData.url) {
      dreamImage.src = imageData.url;
      dreamImage.style.display = "block";
    } else {
      dreamImage.style.display = "none";
      console.error("No image URL returned from DALL·E.");
    }
  } catch (error) {
    console.error("Error generating image via DALL·E:", error);
    dreamImage.style.display = "none";
  }
});

// Handle tweak button click
tweakBtn.addEventListener("click", async () => {
  const tweakText = tweakInput.value.trim();
  if (!tweakText) return;

  try {
    const response = await fetch(DALLE_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: tweakText })
    });
    const data = await response.json();

    if (data && data.url) {
      dreamImage.src = data.url;
      dreamImage.style.display = "block";
    }
  } catch (error) {
    console.error("Error tweaking image:", error);
  }
});

// Grab the burger menu button and the sidebar elements
const burgerMenuBtn = document.getElementById('burgerMenuBtn');
const imageHistorySidebar = document.getElementById('imageHistorySidebar');

// Toggle the sidebar open/close on button click
burgerMenuBtn.addEventListener('click', () => {
  imageHistorySidebar.classList.toggle('open');
});

// Select the image history list and merge button
const imageList = document.getElementById('imageList');
const mergeBtn = document.getElementById('mergeBtn');

let selectedItems = []; // Store selected items

// Add click event to each history item
document.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
        // If already selected, remove it
        if (selectedItems.includes(item)) {
            selectedItems = selectedItems.filter(i => i !== item);
            item.classList.remove('selected');
        }
        // Otherwise, add it (max 2 selections)
        else if (selectedItems.length < 2) {
            selectedItems.push(item);
            item.classList.add('selected');
        }
    });
});

// Handle merging of selected images
mergeBtn.addEventListener('click', () => {
    if (selectedItems.length !== 2) {
        console.log("Please select exactly two images to merge.");
        return;
    }

    // Get the text content of the selected items
    const img1 = selectedItems[0].textContent;
    const img2 = selectedItems[1].textContent;

    console.log(`Merging: ${img1} and ${img2}`);

    // Clear selection
    selectedItems.forEach(item => item.classList.remove('selected'));
    selectedItems = [];
});