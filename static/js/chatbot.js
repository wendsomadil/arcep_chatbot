function sendMessage() {
    let userInput = document.getElementById("userInput").value;

    if (userInput.trim() === "") {
        alert("Veuillez entrer une question.");
        return;
    }

    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `message=${encodeURIComponent(userInput)}`,
    })
    .then(response => response.json())
    .then(data => {
        let responseDiv = document.getElementById("response");
        if (data.error) {
            responseDiv.innerHTML = `<p style="color:red;">Erreur: ${data.error}</p>`;
        } else {
            responseDiv.innerHTML = `<p>${data.response}</p>`;
        }
    })
    .catch(error => {
        console.error("Erreur:", error);
    });
}
