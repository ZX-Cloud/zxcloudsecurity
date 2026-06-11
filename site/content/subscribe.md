+++
title = "Subscribe to ZX Cloud Security"
description = "Get daily cloud security advisories, CVEs, and threat intelligence for AWS, GCP and Azure architects — delivered to your inbox every morning."
slug = "subscribe"
draft = false
+++

<div id="subscribe-status" style="display:none; max-width: 560px; margin: 0 auto 1.5rem; padding: 1rem 1.25rem; border-radius: 8px; text-align: center;"></div>

<div id="subscribe-form" style="max-width: 560px; margin: 2rem auto; text-align: center;">

  <p style="font-size: 16px; line-height: 1.7; margin-bottom: 1.5rem;">
    Join cloud security architects and engineers who start every morning with the ZX Cloud Security daily digest — Critical and High severity advisories across AWS, Azure and GCP, each with a practical <strong>Security Architect's Take</strong> on what to do about it.
  </p>

  <ul style="text-align: left; display: inline-block; margin-bottom: 2rem; line-height: 2;">
    <li>🔴 Critical and High advisories prioritised first</li>
    <li>🤖 AI-enriched with architect-level context</li>
    <li>☁️ Covers AWS, Azure, GCP and general security</li>
    <li>📬 Delivered daily at 06:00 UTC</li>
    <li>✅ Free. No spam. Unsubscribe anytime.</li>
  </ul>

  <div style="margin-bottom: 1.5rem;">
    <p style="font-size: 14px; font-weight: 500; margin-bottom: 0.75rem;">Which advisories would you like to receive?</p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 14px; cursor: pointer;">
        <input type="checkbox" id="cat-all" checked onchange="handleAllChange(this)"> All advisories
      </label>
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 14px; cursor: pointer;">
        <input type="checkbox" id="cat-aws" disabled> AWS
      </label>
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 14px; cursor: pointer;">
        <input type="checkbox" id="cat-azure" disabled> Azure
      </label>
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 14px; cursor: pointer;">
        <input type="checkbox" id="cat-gcp" disabled> GCP
      </label>
      <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 14px; cursor: pointer;">
        <input type="checkbox" id="cat-general" disabled> General
      </label>
    </div>
  </div>

  <div style="display: flex; flex-direction: column; align-items: center; gap: 0.75rem;">
    <input
      type="email"
      id="email-input"
      placeholder="your@email.com"
      required
      style="width: 100%; max-width: 360px; padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid var(--border); background: var(--entry); color: var(--primary); font-size: 15px;"
    />
    <button
      onclick="handleSubscribe()"
      style="width: 100%; max-width: 360px; padding: 0.75rem 1rem; border-radius: 6px; background: var(--primary); color: var(--theme); border: none; cursor: pointer; font-size: 15px; font-weight: 500;"
    >
      Subscribe — it's free
    </button>
  </div>

  <p style="font-size: 12px; color: var(--secondary); margin-top: 1rem;">
    Your email is used solely for sending the ZX Cloud Security digest. Powered by AWS SES.
  </p>

</div>

<script>
function handleAllChange(checkbox) {
  const cats = ['cat-aws', 'cat-azure', 'cat-gcp', 'cat-general'];
  cats.forEach(id => {
    const el = document.getElementById(id);
    el.disabled = checkbox.checked;
    if (checkbox.checked) el.checked = false;
  });
}

function getCategories() {
  if (document.getElementById('cat-all').checked) return ['all'];
  const cats = [];
  if (document.getElementById('cat-aws').checked) cats.push('aws');
  if (document.getElementById('cat-azure').checked) cats.push('azure');
  if (document.getElementById('cat-gcp').checked) cats.push('gcp');
  if (document.getElementById('cat-general').checked) cats.push('general');
  return cats.length > 0 ? cats : ['all'];
}

async function handleSubscribe() {
  const email = document.getElementById('email-input').value.trim();
  if (!email || !email.includes('@')) {
    showStatus('Please enter a valid email address.', '#dc2626', '#fef2f2');
    return;
  }
  const categories = getCategories();
  const btn = document.querySelector('button[onclick="handleSubscribe()"]');
  btn.textContent = 'Subscribing...';
  btn.disabled = true;
  try {
    const resp = await fetch('https://3525nbuoej.execute-api.eu-west-1.amazonaws.com/prod/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, categories })
    });
    const data = await resp.json();
    if (resp.ok) {
      document.getElementById('subscribe-form').style.display = 'none';
      showStatus('✅ Almost there! Check your inbox for a confirmation email from advisories@zxcloudsecurity.co.uk and click the link to confirm your subscription.', '#166534', '#f0fdf4');
    } else {
      showStatus(data.error || 'Something went wrong. Please try again.', '#dc2626', '#fef2f2');
      btn.textContent = 'Subscribe — it\'s free';
      btn.disabled = false;
    }
  } catch (e) {
    showStatus('Something went wrong. Please try again.', '#dc2626', '#fef2f2');
    btn.textContent = 'Subscribe — it\'s free';
    btn.disabled = false;
  }
}

function showStatus(message, color, bg) {
  const el = document.getElementById('subscribe-status');
  el.style.display = 'block';
  el.style.color = color;
  el.style.background = bg;
  el.style.border = '1px solid ' + color;
  el.textContent = message;
}

// Handle redirect status from confirmation link
const params = new URLSearchParams(window.location.search);
const status = params.get('status');
const error = params.get('error');
if (status === 'confirmed') {
  document.getElementById('subscribe-form').style.display = 'none';
  showStatus('🎉 You\'re subscribed! Your first daily digest will arrive tomorrow morning.', '#166534', '#f0fdf4');
} else if (status === 'already_confirmed') {
  document.getElementById('subscribe-form').style.display = 'none';
  showStatus('✅ You\'re already subscribed — look out for your daily digest each morning.', '#166534', '#f0fdf4');
} else if (error) {
  showStatus('There was a problem confirming your subscription. Please try subscribing again.', '#dc2626', '#fef2f2');
}
</script>
