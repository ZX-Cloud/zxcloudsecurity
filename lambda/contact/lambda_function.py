"""
contact/lambda_function.py
ZX Cloud Security — Contact Form Handler

Validates and forwards contact form submissions via SES.
Bot protection: honeypot field check + API Gateway rate limiting.

Environment variables:
  SES_FROM_ADDRESS   e.g. advisories@zxcloudsecurity.co.uk
  SES_TO_ADDRESS     e.g. steve@zxcloudsecurity.co.uk
"""

import json
import os
import re
import boto3

ses = boto3.client('ses', region_name='eu-west-1')

FROM_ADDRESS = os.environ.get('SES_FROM_ADDRESS', 'advisories@zxcloudsecurity.co.uk')
TO_ADDRESS   = os.environ.get('SES_TO_ADDRESS',   'steve@zxcloudsecurity.co.uk')

CORS_HEADERS = {
    'Content-Type':                'application/json',
    'Access-Control-Allow-Origin': 'https://zxcloudsecurity.co.uk',
}


def respond(status: int, message: str) -> dict:
    return {
        'statusCode': status,
        'headers': CORS_HEADERS,
        'body': json.dumps({'message': message}),
    }


def handler(event, context):
    # Parse body
    try:
        body = json.loads(event.get('body') or '{}')
    except (json.JSONDecodeError, TypeError):
        return respond(400, 'Invalid request.')

    # Layer 2: Honeypot — bots fill this hidden field, humans leave it blank
    if body.get('website', '').strip():
        # Silently accept so bots don't know they were filtered
        return respond(200, 'Message received.')

    name    = body.get('name', '').strip()
    email   = body.get('email', '').strip()
    message = body.get('message', '').strip()

    # Basic validation
    if not name or not email or not message:
        return respond(400, 'Please fill in all fields.')

    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return respond(400, 'Please enter a valid email address.')

    if len(message) > 5000:
        return respond(400, 'Message too long (5,000 character limit).')

    # Send via SES
    subject  = f"ZX Cloud Security — Contact form: {name}"
    body_txt = f"From: {name} <{email}>\n\n{message}"
    body_html = f"""<div style="font-family:sans-serif;max-width:600px;">
<p><strong>From:</strong> {name} &lt;{email}&gt;</p>
<hr>
<p style="white-space:pre-wrap;">{message}</p>
</div>"""

    try:
        ses.send_email(
            Source=FROM_ADDRESS,
            Destination={'ToAddresses': [TO_ADDRESS]},
            ReplyToAddresses=[email],
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_txt,  'Charset': 'UTF-8'},
                    'Html': {'Data': body_html, 'Charset': 'UTF-8'},
                },
            },
        )
        print(f"Contact form sent from {email}")
        return respond(200, 'Message sent. We\'ll get back to you within 24 hours.')
    except Exception as e:
        print(f"SES error: {e}")
        return respond(500, 'Failed to send message. Please email advisories@zxcloudsecurity.co.uk directly.')
