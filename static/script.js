document.addEventListener('DOMContentLoaded', function() {
  const analyzeButton = document.getElementById('analyze-button');
  const dreamInput = document.getElementById('dream-input');
  const resultsDiv = document.getElementById('results');
  const analysisText = document.getElementById('analysis-text');
  const dreamImage = document.getElementById('dream-image');

  analyzeButton.addEventListener('click', function() {
    const dream = dreamInput.value;
    if (dream.trim() === '') {
      alert('Please enter your dream.');
      return;
    }

    fetch('/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ dream: dream })
    })
    .then(response => response.json())
    .then(data => {
      analysisText.textContent = data.analysis;
      dreamImage.src = `data:image/png;base64,${data.image_data}`;
      resultsDiv.style.display = 'block';
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while analyzing your dream.');
    });
  });
});