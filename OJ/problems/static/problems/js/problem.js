document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".submission-form");
    const codeEditor = document.getElementById("code-editor");
    const verdictEl = document.getElementById("verdict");
    const langSelect = document.getElementById("lang");

    const simplifyBtn = document.getElementById("simplify-btn");
    const hintBtn = document.getElementById("hint-btn");
    const aiPanel = document.getElementById("ai-panel");
    const aiClose = document.getElementById("ai-panel-close");
    const aiResponse = document.getElementById("ai-panel-response");

    const problemStatement = document.querySelector(".card-box").textContent;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        verdictEl.textContent = "Status: 🚀 Launching...";
        verdictEl.style.color = "#cccccc";

        const lang = langSelect.value;
        const code = codeEditor.value;

        try {
            const res = await fetch("", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken()
                },
                body: new URLSearchParams({ lang, code })
            });

            const data = await res.json();

            verdictEl.textContent = `Status: ${data.verdict}`;

            if (data.verdict === "Success") {
                verdictEl.style.color = "#2ecc71";
                getAIResponse("review", "", code);
            } else {
                verdictEl.style.color =
                    data.verdict === "TLE" ? "#f1c40f" :
                        data.verdict === "MLE" ? "#9b59b6" :
                            "#e74c3c";

                hintBtn.style.display = "inline-block";
            }
        } catch (err) {
            verdictEl.textContent = "Status: ❌ Failed to submit";
            verdictEl.style.color = "#e74c3c";
            console.error(err);
        }
    });

    simplifyBtn.addEventListener("click", () => {
        getAIResponse("simplify", problemStatement, "");
    });

    hintBtn.addEventListener("click", () => {
        getAIResponse("hint", problemStatement, "");
        hintBtn.style.display = "none";
    });

    aiClose.addEventListener("click", () => {
        aiPanel.classList.remove("active");
    });

    function showAIPanel(text) {
        aiResponse.textContent = text;
        aiPanel.classList.add("active");
    }

    async function getAIResponse(action, statement = "", code = "") {
        showAIPanel("🧠 The Universe is thinking...");

        try {
            const res = await fetch("/ai/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    action,
                    statement,
                    code
                })
            });

            const data = await res.json();
            if (data.text) {
                showAIPanel(data.text);
            } else {
                showAIPanel("⚠️ The universe stayed silent. Try again.");
            }
        } catch (err) {
            console.error("AI fetch error:", err);
            showAIPanel("❌ Failed to connect to AI module.");
        }
    }

    function getCSRFToken() {
        const cookie = document.cookie
            .split(";")
            .find(c => c.trim().startsWith("csrftoken="));
        return cookie ? cookie.split("=")[1] : "";
    }
});
