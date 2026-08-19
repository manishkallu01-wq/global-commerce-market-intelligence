variable "project_name" { type = string; default = "commerce-intelligence" }
variable "environment" { type = string; default = "dev" }
variable "aws_region" { type = string; default = "us-east-1" }

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

output "lake_bucket" { value = aws_s3_bucket.lake.id }
output "risk_stream" { value = aws_kinesis_stream.risk_events.name }
