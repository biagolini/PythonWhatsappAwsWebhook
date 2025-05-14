# WhatsApp Webhook Integration with AWS (Serverless Pattern)

## Repository Purpose

This repository provides a validated implementation of a serverless webhook integration for Meta’s WhatsApp Business Platform using AWS Lambda and API Gateway. It enables developers to receive and persist WhatsApp messages via HTTP requests sent by Meta. This solution demonstrates a production-ready approach for message ingestion and storage using a minimal, maintainable AWS stack.

The main Lambda function in this repository is:

* `lambda_function.py` – Handles webhook verification and stores incoming WhatsApp messages in Amazon S3.

For the complete walkthrough of the WhatsApp-side setup, see the related article on Medium: [Configure WhatsApp Business to Send Messages to AWS via Webhook (No AWS Code)](https://medium.com/@biagolini)

---

## Overview

This solution uses AWS-native services to receive HTTP webhook calls from Meta, validate the initial setup token, and store incoming message payloads securely in S3. It is designed to be scalable, cost-efficient, and easily extendable to support future automation or integrations.

---

## Architecture

### Components

* **API Gateway (REST API):** Public entry point for receiving Meta webhook requests.
* **Lambda Function (`lambda_function.py`):**

  * Responds to GET requests for webhook verification using a `VERIFY_TOKEN`.
  * Handles POST requests by saving the payload to an S3 bucket.
* **Amazon S3:** Stores the full JSON payload of each incoming message with a timestamp-based key.

### Message Flow Summary

1. Meta sends a `GET` request to verify the webhook URL.
2. API Gateway forwards the request to the Lambda function.
3. Lambda compares the `hub.verify_token` against the environment variable.
4. If valid, returns the challenge string to complete verification.
5. After verification, Meta sends `POST` requests containing WhatsApp messages.
6. Lambda stores each payload as a JSON file in S3.

---

## Setup Instructions

### 1. Create Lambda Function

* Name: `whatsappWebhookHandler`
* Runtime: Python 3.13+
* Environment Variable:
  * `VERIFY_TOKEN = <your_token_here>`
* IAM Role Permissions:
  * `s3:PutObject` for your target bucket
  * CloudWatch logging

Deploy the function using the code in `lambda_function.py`.

### 2. Create S3 Bucket

* Name: `your-inbound-webhook-bucket` (or any name you choose)
* Ensure Lambda has permission to write to this bucket.

### 3. Create API Gateway (REST)

* Create a REST API named `WhatsAppWebhookAPI`
* Resource Path: `/webhook`
* Method: `ANY`

  * Integration type: Lambda Proxy
  * Target: `whatsappWebhookHandler`

Deploy the API to a stage (e.g., `prod`) and note the **Invoke URL**.

### 4. Meta Platform Configuration

From Meta for Developers:

* Add a WhatsApp product to your app.
* Set Webhook Callback URL to:
  `https://<api-id>.execute-api.<region>.amazonaws.com/prod/webhook`
* Use the same `VERIFY_TOKEN` configured in your Lambda.
* Subscribe to the `messages` field under **Webhook Fields**.

---

## Testing

### Simulate Meta Webhook (GET)

```bash
curl -X GET "https://<api-id>.execute-api.<region>.amazonaws.com/prod/webhook?hub.mode=subscribe&hub.verify_token=<your_token>&hub.challenge=1234"
```

Expected response:

```
Status: 200 OK
Body: 1234
```

### Simulate WhatsApp Message (POST)

```bash
curl -X POST "https://<api-id>.execute-api.<region>.amazonaws.com/prod/webhook" \
  -H "Content-Type: application/json" \
  -d '{ "object": "whatsapp_business_account", "entry": [ ... ] }'
```

Check your S3 bucket to verify the message was stored.

---

## Security Notes

* Always use a strong `VERIFY_TOKEN`.
* Limit Lambda permissions to the specific S3 bucket used.
* Ensure API Gateway is not publicly writable beyond Meta’s use case (e.g., via usage plans or WAF if needed).

---

## References

* [Medium Tutorial – Full Configuration Guide](https://medium.com/@biagolini)
* [Meta Webhook Documentation](https://developers.facebook.com/docs/graph-api/webhooks/getting-started/)
* [WhatsApp Business API Setup](https://developers.facebook.com/docs/whatsapp/)
