+++
title = "Unsubscribe"
description = "Unsubscribe from the ZX Cloud Security daily digest."
slug = "unsubscribe"
draft = false
+++

<div id="status-box" style="max-width: 500px; margin: 2rem auto; text-align: center; padding: 2rem; border-radius: 8px; border: 1px solid var(--border);">
  <p id="status-message" style="font-size: 15px; line-height: 1.7;">Processing your request...</p>
  <a href="/" style="font-size: 14px; color: var(--secondary);">← Back to ZX Cloud Security</a>
</div>

<script>
const params = new URLSearchParams(window.location.search);
const status = params.get('status');
const msg = document.getElementById('status-message');
const box = document.getElementById('status-box');

if (status === 'success') {
  msg.textContent = "✅ You've been unsubscribed successfully. You won't receive any further emails from ZX Cloud Security.";
  box.style.background = '#f0fdf4';
  box.style.borderColor = '#16a34a';
} else if (status === 'invalid') {
  msg.textContent = "⚠️ Invalid unsubscribe link. Please contact advisories@zxcloudsecurity.co.uk if you need help.";
  box.style.background = '#fffbeb';
  box.style.borderColor = '#d97706';
} else if (status === 'error') {
  msg.textContent = "❌ Something went wrong. Please contact advisories@zxcloudsecurity.co.uk to unsubscribe manually.";
  box.style.background = '#fef2f2';
  box.style.borderColor = '#dc2626';
} else {
  msg.textContent = "Use the unsubscribe link in your daily digest email to unsubscribe.";
}
</script>
