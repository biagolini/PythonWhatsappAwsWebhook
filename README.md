# WhatsApp Webhook Integration with AWS (Serverless Pattern)

## About This Repository

This repository accompanies a series of technical articles published on [my Medium blog](https://medium.com/@biagolini), where I explore the design and implementation of a WhatsApp Business API integration using serverless AWS services.

The main goal of this project is to provide a clean, modular reference for building cloud-native, intelligent, and maintainable chatbot systems powered by:

* AWS Lambda for compute
* Amazon Bedrock Agents for inference and conversation orchestration
* Amazon S3 for message/event logging
* Meta Graph API for WhatsApp messaging

Each Python script in this repository corresponds to a specific article and focuses on an isolated feature of the integration. This structure makes it easier to follow and reuse code as you read the posts or adapt the project to your own use case.

## Code Structure

| File                              | Description                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------- |
| `lambda_function_01_subscribe.py` | Webhook verification logic for Meta (responds to GET request with challenge)                  |
| `lambda_function_02_response.py`  | Basic responder that handles messages and returns a fixed string                              |
| `lambda_function_03_bedrock.py`   | Full pipeline: receives a message, invokes an Amazon Bedrock Agent, and replies over WhatsApp |

New scripts will be added as the article series expands to cover topics like session management, error handling, contextual memory, and multi-agent architectures.

## Lambda Environment Variables

Each Lambda function may require different environment variables. Below is a consolidated list of the most important ones across the project:

| Variable           | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `ACCESS_TOKEN`     | Meta Graph API token for WhatsApp authorization      |
| `API_VERSION`      | Meta API version (e.g., `v22.0`)                     |
| `BEDROCK_AGENT_ID` | ID of your Amazon Bedrock Agent                      |
| `BEDROCK_ALIAS_ID` | Alias ID used to invoke the Bedrock Agent            |
| `BUCKET_NAME`      | Name of the S3 bucket used to log requests/responses |
| `PHONE_NUMBER_ID`  | WhatsApp Business phone number ID                    |
| `VERIFY_TOKEN`     | Verification token used to validate webhook setup    |

Each Python script includes inline documentation and comments explaining which variables are required and how they are used.

## Related Articles on Medium

This repository is tightly coupled with a series of walkthrough articles available on my blog:

[https://medium.com/@biagolini](https://medium.com/@biagolini)

The articles cover topics such as:

* Setting up a WhatsApp Business webhook with AWS
* Serverless message handling
* Integrating Bedrock Agents for intelligent replies
* Logging and monitoring chatbot interactions
* Building a scalable architecture using API Gateway, Lambda, and S3

## Tech Keywords (for context and discovery)

WhatsApp Integration, Amazon Bedrock, AWS Lambda, API Gateway, Meta Graph API, Intelligent Replies, Serverless Architecture, S3 Logging, Conversational AI, Payload Inspection, Real-time Messaging, Automation, Chatbot Infrastructure, Cloud-Native Deployment
