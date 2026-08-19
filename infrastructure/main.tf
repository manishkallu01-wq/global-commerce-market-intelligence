variable "project_name" {
  type    = string
  default = "commerce-intelligence"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "enable_warehouse" {
  type        = bool
  default     = false
  description = "Create billable Redshift Serverless resources when explicitly enabled."
}

provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "lake" {
  bucket_prefix = "${var.project_name}-${var.environment}-lake-"
  force_destroy = false
  tags = { Project = var.project_name, Environment = var.environment }
}

resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}

resource "aws_s3_bucket_public_access_block" "lake" {
  bucket                  = aws_s3_bucket.lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    id     = "raw-retention"
    status = "Enabled"
    filter { prefix = "raw/" }
    transition {
      days          = 30
      storage_class = "INTELLIGENT_TIERING"
    }
    transition {
      days          = 180
      storage_class = "GLACIER_IR"
    }
  }
}

resource "aws_kinesis_stream" "risk_events" {
  name = "${var.project_name}-${var.environment}-risk-events"
  stream_mode_details { stream_mode = "ON_DEMAND" }
  encryption_type = "KMS"
  kms_key_id = "alias/aws/kinesis"
  tags = { Project = var.project_name, Environment = var.environment }
}

resource "aws_glue_catalog_database" "commerce" {
  name = replace("${var.project_name}_${var.environment}", "-", "_")
}

resource "aws_cloudwatch_log_group" "pipeline" {
  name              = "/aws/${var.project_name}/${var.environment}/pipeline"
  retention_in_days = 30
}

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-${var.environment}-alerts"
}

resource "aws_cloudwatch_metric_alarm" "kinesis_write_throttle" {
  alarm_name          = "${var.project_name}-${var.environment}-kinesis-write-throttle"
  namespace           = "AWS/Kinesis"
  metric_name         = "WriteProvisionedThroughputExceeded"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions          = { StreamName = aws_kinesis_stream.risk_events.name }
}

data "aws_iam_policy_document" "orchestrator_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "orchestrator" {
  name_prefix       = "${var.project_name}-${var.environment}-sfn-"
  assume_role_policy = data.aws_iam_policy_document.orchestrator_assume.json
}

resource "aws_iam_role_policy" "orchestrator" {
  role = aws_iam_role.orchestrator.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Action = ["lambda:InvokeFunction", "events:PutTargets", "events:PutRule", "events:DescribeRule"], Resource = "*" }] })
}

resource "aws_sfn_state_machine" "pipeline" {
  name       = "${var.project_name}-${var.environment}-pipeline"
  role_arn   = aws_iam_role.orchestrator.arn
  definition = file("${path.module}/state_machine.asl.json")
}

resource "aws_redshiftserverless_namespace" "commerce" {
  count         = var.enable_warehouse ? 1 : 0
  namespace_name = "${var.project_name}-${var.environment}"
  db_name        = "commerce"
}

resource "aws_redshiftserverless_workgroup" "commerce" {
  count          = var.enable_warehouse ? 1 : 0
  workgroup_name = "${var.project_name}-${var.environment}"
  namespace_name = aws_redshiftserverless_namespace.commerce[0].namespace_name
  publicly_accessible = false
  base_capacity = 8
}

resource "aws_budgets_budget" "monthly" {
  name         = "${var.project_name}-${var.environment}-monthly"
  budget_type  = "COST"
  limit_amount = "250"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
}

output "lake_bucket" {
  value = aws_s3_bucket.lake.id
}
output "risk_stream" {
  value = aws_kinesis_stream.risk_events.name
}
