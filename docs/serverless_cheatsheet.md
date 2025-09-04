# Serverless Computing — Cheat Sheet

**Quick Summary**  
Serverless computing runs code without managing servers. AWS handles infrastructure, scaling, availability, and maintenance. You focus on application logic. Examples: **AWS Lambda** (serverless), **Amazon ECS/EKS** (container services), **AWS Elastic Beanstalk** (managed PaaS).

---

## Levels of Control (Most → Least)
- **EC2 (Unmanaged):** Full VM/OS control. You manage OS, patches, runtime, scaling.  
- **Managed (ECS/EKS/Elastic Beanstalk):** AWS handles orchestration/operations aspects. You manage app containers/config.  
- **Serverless (Lambda):** AWS manages everything infra-related. You provide code + config (memory, timeout, IAM).

---

## Customer vs AWS Responsibilities (Shared Responsibility)
- **AWS (of the cloud):** Physical hardware, hosts, networking, hypervisors, global infra, scaling, and patching (for serverless).  
- **Customer (in the cloud):** Application code, data, IAM policies, environment variables, input validation, logging, monitoring, and secrets handling.

---

## When to Choose What
- **Choose EC2** when you need kernel/OS access, custom drivers, or long-running stateful processes.  
- **Choose Managed (ECS/EKS)** for container portability, microservices, or longer-running workloads with orchestration.  
- **Choose Lambda** for event-driven workloads, bursty traffic, pay-per-use cost savings, and when you don't want infra ops.

**Avoid serverless when:** long-running processes (>15 min), strict cold-start sensitivity, OS-level control required, or complex custom networking.

---

## Key Exam Bullets (Memorize)
- Serverless = no server provisioning; billing = invocations * duration * memory.  
- EC2 = customer manages OS and app; AWS manages physical hardware.  
- Managed containers provide a middle-ground: portability + less infra ops.  
- In serverless, secure your code, grant least-privilege IAM roles, and monitor logs (CloudWatch).  
- Watch for limits (execution time, ephemeral storage, memory) and cold starts.

---

## Simple Analogies
- **EC2** = renting an empty apartment (you bring furniture & utilities).  
- **Managed service** = serviced apartment (some utilities handled).  
- **Serverless** = food delivery (you order the meal; someone cooks, serves and cleans).  
- **Shared responsibility** = AWS secures the building; you secure the contents of your apartment.

---

## Flashcards (Q/A)
1. **Q:** What is serverless computing?  
   **A:** Running code without managing servers; provider handles infra and scaling.

2. **Q:** Give a serverless compute service in AWS.  
   **A:** AWS Lambda.

3. **Q:** Who manages the OS in an EC2 instance?  
   **A:** The customer.

4. **Q:** Billing model difference EC2 vs Lambda?  
   **A:** EC2 = instance/hour (or per-second) pricing; Lambda = per-invocation + duration + memory.

5. **Q:** Name two reasons not to use serverless.  
   **A:** Need for long-running processes or OS-level control; strict low-latency/cold-start sensitive workloads.

---

## Quick Practice Labs (30–60 minutes)
1. Create a Lambda "Hello World" and view logs in CloudWatch.  
2. Trigger Lambda with an S3 PUT event (upload file → Lambda invoked).  
3. Implement the same micro-task on EC2 and Lambda; compare cost & latency.  
4. Create a minimal IAM role for Lambda to read a specific S3 bucket (least privilege).

---

*File generated for Solomon Baloyi — ready to add to your GitHub repo under `/docs` or `/learning`.*
