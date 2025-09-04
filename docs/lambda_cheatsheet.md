# AWS Lambda — Cheat Sheet

**Quick Summary**  
AWS Lambda is a serverless compute service that runs code in response to events without provisioning or managing servers. AWS manages execution environments, scaling, and availability. You supply function code, configuration (handler, runtime, memory, timeout), and an IAM execution role. Billing is per-request and for execution duration × memory.

---

## Key Components
- **Function**: your code + configuration (handler, runtime, memory, timeout, env vars).  
- **Trigger / Event Source**: what invokes the function (API Gateway, S3, SQS, SNS, EventBridge, CloudWatch, etc.).  
- **Execution role (IAM)**: grants the function permissions to access AWS resources (least privilege).  
- **Event source mapping**: connects services like SQS/DynamoDB streams to Lambda (polling + batch processing).  
- **Monitoring & Logging**: CloudWatch Logs, CloudWatch Metrics, AWS X-Ray tracing.  
- **Concurrency & Scaling**: Lambda scales automatically; control with reserved or provisioned concurrency.

---

## Exam-ready bullets
- Lambda runs code in response to events; no server provisioning required.  
- Billing = number of requests + execution duration (ms) × memory configured.  
- Triggers: API Gateway, S3, SQS, SNS, DynamoDB streams, EventBridge, CloudWatch.  
- Use IAM execution role with least privilege.  
- Synchronous vs asynchronous invocation: asynchronous may retry and can have DLQ/on-failure destinations.  
- Configure batch size & visibility timeout for SQS event source mappings.  
- Cold starts can add latency; provisioned concurrency reduces cold starts.

---

## Small Python handler (SQS example)
Save as `lambda_function.py` and zip for deployment:

```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    for record in event.get('Records', []):
        msg_id = record.get('messageId')
        body = record.get('body')
        logger.info(f"Processing message {msg_id}: {body}")
        try:
            data = json.loads(body)
            # business logic here
        except Exception as e:
            logger.exception("Failed to process message")
            # raising exception will cause retries depending on mapping/config
    return {"status": "ok", "processed": len(event.get('Records', []))}
```

---

## CLI: Quick SQS → Lambda wiring (example)
Replace placeholders (REGION, ACCOUNT_ID, ROLE_ARN, QUEUE_NAME):

```bash
# Create SQS queue
aws sqs create-queue --queue-name my-lambda-queue

# Create Lambda (zip your handler)
aws lambda create-function   --function-name mySqsProcessor   --runtime python3.9   --role arn:aws:iam::ACCOUNT_ID:role/LambdaSQSRole   --handler lambda_function.handler   --zip-file fileb://function.zip   --timeout 30   --memory-size 256

# Create event source mapping (SQS -> Lambda)
aws lambda create-event-source-mapping   --function-name mySqsProcessor   --batch-size 10   --event-source-arn arn:aws:sqs:REGION:ACCOUNT_ID:my-lambda-queue
```

---

## Best Practices & Gotchas
- Principle of least privilege for the execution role.  
- Make handlers idempotent: retries are possible.  
- Tune batch size and visibility timeout for SQS to avoid duplicate processing.  
- Use DLQs or Failure Destinations for async failures.  
- Monitor with CloudWatch (Invocations, Errors, Duration, Throttles) and use X-Ray for tracing.  
- Beware cold starts for latency-sensitive workloads; consider provisioned concurrency.  
- Test locally with AWS SAM or LocalStack before deploying.

---

## Simple Analogies
- **Lambda** = vending machine: press a button (event) and receive a snack (function runs); you pay only for what you use.  
- **Event-source mapping** = a waiter polling tables (queue) and bringing batches of orders to the chef (function).  
- **Cold start** = opening a shop in the morning — first customer waits while you prep; later customers are faster.

---

## Flashcards (Q/A)
1. **Q:** What is AWS Lambda?  
**A:** A serverless compute service that runs code in response to events.  
2. **Q:** Name three Lambda triggers.  
**A:** API Gateway, S3, SQS (also SNS, EventBridge, DynamoDB streams).  
3. **Q:** Where do Lambda logs appear?  
**A:** CloudWatch Logs.  
4. **Q:** What reduces cold starts?  
**A:** Provisioned concurrency.  
5. **Q:** Why make Lambda handlers idempotent?  
**A:** Because retries can cause duplicate processing.  

---

## Quick Practice Tasks (20–60 min)
1. Create a Lambda that logs "Hello, <yourname>" and invoke it manually.  
2. Create an SQS queue, send 5 messages, and configure Lambda with batch size=2; inspect CloudWatch Logs.  
3. Cause one message to fail and observe retry behavior and DLQ handling.  
4. Compare performance/cost of a small CPU-bound job on EC2 vs Lambda (change memory size and observe duration).

---

*Generated for Solomon Baloyi — ready to add to your repo under `/docs` or `/learning`.*
