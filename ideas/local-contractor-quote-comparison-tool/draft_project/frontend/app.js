const form = document.querySelector("#idea-form");
const input = document.querySelector("#idea-input");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = "Running...";
  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ input: input.value }),
    });
    const data = await response.json();
    result.textContent = data.recommendation;
  } catch (error) {
    result.textContent = `POC request failed: ${error}`;
  }
});
