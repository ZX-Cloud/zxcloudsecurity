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
  msg.innerHTML = "<strong style='font-size:17px;'>✅ Unsubscribed successfully</strong><br><span style='color:#374151;'>You won't receive any further emails from ZX Cloud Security.</span>";
  box.style.background = '#f0fdf4';
  box.style.borderColor = '#16a34a';
  msg.style.color = '#14532d';
} else if (status === 'invalid') {
  msg.innerHTML = "<strong style='font-size:17px;'>⚠️ Invalid link</strong><br><span style='color:#374151;'>Please contact <a href='mailto:advisories@zxcloudsecurity.co.uk'>advisories@zxcloudsecurity.co.uk</a> if you need help.</span>";
  box.style.background = '#fffbeb';
  box.style.borderColor = '#d97706';
  msg.style.color = '#78350f';
} else if (status === 'error') {
  msg.innerHTML = "<strong style='font-size:17px;'>❌ Something went wrong</strong><br><span style='color:#374151;'>Please contact <a href='mailto:advisories@zxcloudsecurity.co.uk'>advisories@zxcloudsecurity.co.uk</a> to unsubscribe manually.</span>";
  box.style.background = '#fef2f2';
  box.style.borderColor = '#dc2626';
  msg.style.color = '#7f1d1d';
} else {
  msg.textContent = "Use the unsubscribe link in your daily digest email to unsubscribe.";
}
</script>
