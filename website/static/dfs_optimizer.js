
// Listen for form submission
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Get form data
    const race = document.getElementById('race').value;
    const lineups = document.getElementById('lineups').value;

    // Make an AJAX request to the Flask route
    fetch('/dfs-optimizer', {
        method: 'POST',
        body: JSON.stringify({ race: race, lineups: lineups }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update the HTML with the optimizer results
        const resultsDiv = document.getElementById('optimizer-results');
        resultsDiv.innerHTML = `<p>Results:</p><pre>${JSON.stringify(data, null, 2)}</pre>`;
    });
});
