document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById("answerForm");
  const responseMsg = document.getElementById("responseMsg");

  if (form && responseMsg) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const payload = {
        student_id: document.getElementById("studentId").value,
        topic: document.getElementById("topic").value,
        answer: document.getElementById("answer").value,
      };

      try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/submit-answer`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await res.json();
        responseMsg.textContent = "✅ Answer submitted successfully!";
        responseMsg.className = "mt-4 text-sm text-green-600";
      } catch (err) {
        responseMsg.textContent = "❌ Failed to submit answer";
        responseMsg.className = "mt-4 text-sm text-red-600";
      }
    });
  }
});
