terraform {
  backend "s3" {
    bucket         = "uday-terraform-state-2026"
    key            = "day17/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
