document.getElementById('username').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') { performSearch(); }
});

async function performSearch() {
    const username = document.getElementById('username').value.trim();
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');

    if (!username) {
        resultsDiv.innerHTML = "<p class='not-found'>Please enter a username first!</p>";
        return;
    }

    resultsDiv.innerHTML = "";
    loadingDiv.classList.remove("hidden");
    document.getElementById("progress-text").innerText = "Initializing scan...";

    try {
        // Updated URL: Ab ye hosting server par bhi kaam karega
        const response = await fetch(`/search?username=${username}`);
        const data = await response.json();

        resultsDiv.innerHTML = "";
        data.forEach(item => {
            const p = document.createElement('div');
            p.className = "result-item";
            p.innerHTML = `
                <span class="${item.status === "Found" ? "found" : "not-found"}">${item.platform}</span>
                <span>
                    ${item.status}
                    ${item.status === "Found" ? ` - <a href="${item.url}" target="_blank" style="color:#00e5ff">Check</a>` : ""}
                </span>`;
            resultsDiv.appendChild(p);
        });

        document.getElementById("progress-text").innerText = "Scan completed ✔";
        setTimeout(() => loadingDiv.classList.add("hidden"), 1000);

    } catch (error) {
        loadingDiv.classList.add("hidden");
        resultsDiv.innerHTML = "<p class='not-found'>Error: Backend unreachable!</p>";
    }
}
  
