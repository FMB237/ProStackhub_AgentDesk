const btn = document.getElementById('researchBtn');
const goalEl = document.getElementById('goal');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const reportEl = document.getElementById('report');
const logEl = document.getElementById('log');

btn.addEventListener('click', async () => {
    const goal = goalEl.value.trim();
    if (!goal) {
        statusEl.textContent = 'Please enter a research goal.';
        return;
    }
    btn.disabled = true;
    statusEl.textContent = 'Researching...';
    resultsEl.hidden = true;

    try {
        const res = await fetch('/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ goal })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Request failed');
        }
        const data = await res.json();
        reportEl.textContent = data.report;
        logEl.innerHTML = '';
        data.log.forEach(entry => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${entry.step}</strong>: ${entry.detail}`;
            logEl.appendChild(li);
        });
        resultsEl.hidden = false;
        statusEl.textContent = 'Done.';
    } catch (e) {
        statusEl.textContent = 'Error: ' + e.message;
    } finally {
        btn.disabled = false;
    }
});
