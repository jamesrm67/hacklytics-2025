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