# can also save terraform in s3
provider "aws" {
    version = "4.53.0"
    region  = "ap-southeast-1" 
    profile = "codepipeline"
}

# store the terraform state file in s3
terraform {
  backend "s3" {
    bucket  = "worldgate-tracktrace-terraform-state"
    key     = "backend/terraform.tfstate"
    region  = "ap-southeast-1"
    profile = "codepipeline"
  }
}