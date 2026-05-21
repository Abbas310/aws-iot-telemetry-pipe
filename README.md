# Serverless IoT Telemetry Pipeline

An event-driven cloud architecture built to ingest, process, store, and expose real-time IoT device telemetry data.

## Architecture Flow
1. **Ingestion**: JSON payloads are uploaded to an Amazon S3 bucket.
2. **Processing**: S3 triggers a Python Lambda function that handles data sanitization (converting numeric types to Python Decimals for DynamoDB).
3. **Storage**: Data is committed to an Amazon DynamoDB table.
4. **Alerting**: If device status is non-normal, an Amazon SNS alert is dispatched to an administrator's email.
5. **Consumption**: Amazon API Gateway routes incoming client HTTP GET requests to a secondary Fetcher Lambda function to return the historical dataset.
