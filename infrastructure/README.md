# Infrastructure

Terraform provisions encrypted and versioned S3 storage, lifecycle rules, Kinesis, Glue, Step Functions, IAM, CloudWatch, SNS alerts and an AWS budget. Redshift Serverless is guarded by `enable_warehouse=false` because it creates billable capacity. Databricks jobs are deployed separately through `databricks.yml`.

```bash
terraform init
terraform plan -var='environment=dev'
# Review costs before explicitly enabling the warehouse:
terraform plan -var='enable_warehouse=true'
```
