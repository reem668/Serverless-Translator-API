# Serverless Translator – AWS Lambda + S3 + DynamoDB + SNS + Static Website

## Overview
This project is a **fully serverless file translation system** built during my cloud computing training.  
It uses AWS managed services with **no traditional backend server** — logic runs in AWS Lambda.

**Initial API version:**
- Upload file to S3
- Lambda (S3 trigger) translates it to English with Amazon Translate
- Detects sentiment with Amazon Comprehend
- Stores results in DynamoDB
- Sends SNS alert if sentiment is negative

**Upgraded static website version:**
- HTML + JavaScript frontend hosted on S3
- `fetch()` calls to API Gateway to get pre-signed S3 upload URL
- Uploads file to S3 directly from the browser
- Fetches processed results from DynamoDB via API Gateway
- Displays translation, sentiment, and original text

## Skills Used
- AWS Lambda
- Amazon S3
- DynamoDB
- Amazon Translate
- Amazon Comprehend
- Amazon SNS
- API Gateway
- Static Website Hosting

## Deployment Steps
1. Create S3 bucket for uploads & static site.
2. Create DynamoDB table (`filename` as PK).
3. Create SNS topic for alerts.
4. Deploy Lambdas:
   - `lambda_process_upload.py` (S3 trigger)
   - `lambda_get_results.py` (API Gateway GET)
5. Create IAM role with `policy.json`.
6. Host `index.html` on S3 (optional: CloudFront for CDN).

