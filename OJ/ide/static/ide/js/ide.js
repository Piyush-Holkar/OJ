document.addEventListener("DOMContentLoaded", () => {
    const runBtn = document.getElementById("run-button");
    const codeEditor = document.getElementById("code-editor");
    const inputEditor = document.getElementById("input-editor");
    const verdictEl = document.getElementById("verdict");
    const timeUsedEl = document.getElementById("time-used");
    const outputBox = document.getElementById("output-box");

    // Tab support inside textarea
    [codeEditor, inputEditor].forEach(editor => {
        editor.addEventListener("keydown", (e) => {
            if (e.key === "Tab") {
                e.preventDefault();
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                editor.value = editor.value.substring(0, start) + "\t" + editor.value.substring(end);
                editor.selectionStart = editor.selectionEnd = start + 1;
            }
        });
    });

    runBtn.addEventListener("click", async () => {
        const language = document.getElementById("language-select").value;
        const code = codeEditor.value;
        const input = inputEditor.value;

        verdictEl.textContent = "Status: 🚀 Launching...";
        verdictEl.className = "";

        const res = await fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()
            },
            body: new URLSearchParams({
                language,
                code,
                input
            })
        });

        const data = await res.json();

        verdictEl.textContent = `Status: ${data.verdict}`;
        verdictEl.className = data.verdict.toLowerCase() === "success" ? "success" : "failure";

        timeUsedEl.textContent = data.time_used || "⏱ N/A";
        outputBox.textContent = data.verdict === "Success" ? data.output : data.error;
    });

    function getCSRFToken() {
        const cookie = document.cookie.split(";").find(c => c.trim().startsWith("csrftoken="));
        return cookie ? cookie.split("=")[1] : "";
    }
});
