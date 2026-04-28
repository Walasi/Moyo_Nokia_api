document.getElementById('claimBtn').addEventListener('click', async () => {
  const phone = document.getElementById('phone').value.trim();
  const location = document.getElementById('location').value;
  const statusDiv = document.getElementById('status');

  if (!phone) {
    statusDiv.className = 'status error';
    statusDiv.textContent = 'Please enter a phone number';
    statusDiv.classList.remove('hidden');
    return;
  }

  statusDiv.className = 'status';
  statusDiv.textContent = '⏳ Verifying with Nokia APIs...';
  statusDiv.classList.remove('hidden');

  try {
    const response = await fetch('http://localhost:8000/api/claim', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: phone, location: location })
    });

    if (!response.ok) {
      let errorMsg = `Server error ${response.status}`;
      try {
        const errData = await response.json();
        errorMsg = errData.detail || errData.message || errorMsg;
      } catch (e) {}
      throw new Error(errorMsg);
    }

    const data = await response.json();
    console.log('Claim response data:', data);   // <== critical for debugging

    if (data.status === 'approved') {
      statusDiv.className = 'status success';
      statusDiv.innerHTML = `✅ Claim approved!<br>
        SIM: ${data.checks.sim_swap.status}<br>
        Location: ${data.checks.location.network_location} (verified)<br>
        <strong>Stellar TX:</strong> <a href="https://horizon-testnet.stellar.org/transactions/${data.tx_id}" target="_blank">${data.tx_id.slice(0, 10)}...</a>`;
    } else {
      // Blocked state
      statusDiv.className = 'status error';
      let html = `❌ Blocked: ${data.reason}<br>
        SIM: ${data.checks?.sim_swap?.status || 'n/a'}<br>
        Location match: ${data.checks?.location?.match ?? 'n/a'}`;

      // Show recovery button ONLY if reason contains 'SIM recently swapped'
      if (data.reason && data.reason.includes('SIM recently swapped')) {
        html += `
          <br><button id="recoverBtn" style="margin-top:10px; background:#f39c12; border:none; color:white; padding:0.5rem 1rem; border-radius:4px;">
            Recover My Account
          </button>
          <div id="recoveryArea" style="margin-top:10px; display:none;">
            <input type="text" id="secretWord" placeholder="Enter secret word" style="padding:0.5rem; width:100%; margin-bottom:5px;">
            <button id="submitRecovery" style="background:#3498db; color:white; border:none; padding:0.5rem 1rem; border-radius:4px;">Submit</button>
            <p id="recoveryMsg"></p>
          </div>`;
      }

      statusDiv.innerHTML = html;

      // Attach listeners after the DOM is updated
      if (data.reason && data.reason.includes('SIM recently swapped')) {
        // Small delay to ensure elements exist
        setTimeout(() => {
          const recoverBtn = document.getElementById('recoverBtn');
          const submitRecovery = document.getElementById('submitRecovery');
          if (recoverBtn) {
            recoverBtn.addEventListener('click', () => {
              document.getElementById('recoveryArea').style.display = 'block';
            });
          }
          if (submitRecovery) {
            submitRecovery.addEventListener('click', async () => {
              const secret = document.getElementById('secretWord').value.trim();
              const recoveryMsg = document.getElementById('recoveryMsg');
              try {
                const res = await fetch('http://localhost:8000/api/recover', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ phone_number: phone, secret_word: secret })
                });
                if (!res.ok) {
                  const err = await res.json();
                  throw new Error(err.detail || 'Recovery failed');
                }
                const result = await res.json();
                recoveryMsg.textContent = result.message;
                // Auto re-try claim after 2 seconds
                setTimeout(() => {
                  document.getElementById('recoveryArea').style.display = 'none';
                  document.getElementById('claimBtn').click();
                }, 2000);
              } catch (err) {
                recoveryMsg.textContent = 'Error: ' + err.message;
              }
            });
          }
        }, 100);
      }
    }
  } catch (error) {
    statusDiv.className = 'status error';
    let msg = 'Unknown error';
    if (typeof error === 'string') msg = error;
    else if (error.message) msg = error.message;
    else if (error.detail) msg = error.detail;
    else msg = JSON.stringify(error);
    statusDiv.textContent = 'Error: ' + msg;
  }
});