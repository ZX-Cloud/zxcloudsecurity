+++
title = "Contact"
description = "Get in touch with ZX Cloud Security — editorial enquiries, corrections, and subscription support."
slug = "contact"
draft = false
+++

## Get in Touch

Use the form below for editorial enquiries, corrections, feedback, or subscription support. We aim to respond within 24 hours.

<div style="max-width:540px;margin:2rem 0;">
  <div id="contact-form-wrap">
    <div style="margin-bottom:1rem;">
      <label for="cf-name" style="display:block;font-size:14px;font-weight:600;margin-bottom:4px;">Name</label>
      <input type="text" id="cf-name" placeholder="Your name" autocomplete="name"
        style="width:100%;padding:0.6rem 0.8rem;border-radius:6px;border:1px solid var(--border);background:var(--entry);color:var(--primary);font-size:14px;" />
    </div>
    <div style="margin-bottom:1rem;">
      <label for="cf-email" style="display:block;font-size:14px;font-weight:600;margin-bottom:4px;">Email</label>
      <input type="email" id="cf-email" placeholder="your@email.com" autocomplete="email"
        style="width:100%;padding:0.6rem 0.8rem;border-radius:6px;border:1px solid var(--border);background:var(--entry);color:var(--primary);font-size:14px;" />
    </div>
    <div style="margin-bottom:1rem;">
      <label for="cf-message" style="display:block;font-size:14px;font-weight:600;margin-bottom:4px;">Message</label>
      <textarea id="cf-message" rows="6" placeholder="Your message..."
        style="width:100%;padding:0.6rem 0.8rem;border-radius:6px;border:1px solid var(--border);background:var(--entry);color:var(--primary);font-size:14px;resize:vertical;"></textarea>
    </div>
    <!-- Honeypot: hidden from humans, bots fill this in -->
    <div style="display:none;" aria-hidden="true">
      <input type="text" id="cf-website" name="website" tabindex="-1" autocomplete="off" />
    </div>
    <button onclick="submitContact()"
      style="padding:0.6rem 1.5rem;border-radius:6px;background:var(--primary);color:var(--theme);border:none;cursor:pointer;font-size:14px;font-weight:600;">
      Send Message
    </button>
    <div id="cf-msg" style="margin-top:1rem;font-size:14px;display:none;"></div>
  </div>
</div>

---

**Subscription support**
Use the unsubscribe link in any digest email to unsubscribe. If you have trouble, use the form above and we'll remove you manually within 24 hours.

---

**Privacy and data enquiries**
See the [Privacy Policy](/privacy/) for details of how your data is handled. For requests to access or delete your data, use the form above.

---

**About the site**
See the [About](/about/) page for background on ZX Cloud Security and the author.

<script>
async function submitContact() {
  const name    = document.getElementById('cf-name').value.trim();
  const email   = document.getElementById('cf-email').value.trim();
  const message = document.getElementById('cf-message').value.trim();
  const website = document.getElementById('cf-website').value;
  const msg     = document.getElementById('cf-msg');

  if (!name || !email || !message) {
    msg.style.display = 'block';
    msg.style.color = '#dc2626';
    msg.textContent = 'Please fill in all fields.';
    return;
  }

  const btn = document.querySelector('button[onclick="submitContact()"]');
  btn.disabled = true;
  btn.textContent = 'Sending...';
  msg.style.display = 'none';

  try {
    const resp = await fetch('https://3525nbuoej.execute-api.eu-west-1.amazonaws.com/prod/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message, website })
    });
    const data = await resp.json();
    msg.style.display = 'block';
    if (resp.ok) {
      msg.style.color = '#16a34a';
      msg.textContent = '✅ ' + data.message;
      document.getElementById('cf-name').value = '';
      document.getElementById('cf-email').value = '';
      document.getElementById('cf-message').value = '';
      btn.style.display = 'none';
    } else {
      msg.style.color = '#dc2626';
      msg.textContent = data.message || 'Something went wrong. Please try again.';
      btn.disabled = false;
      btn.textContent = 'Send Message';
    }
  } catch (e) {
    msg.style.display = 'block';
    msg.style.color = '#dc2626';
    msg.textContent = 'Something went wrong. Please try again.';
    btn.disabled = false;
    btn.textContent = 'Send Message';
  }
}
</script>
