# AMI_Packer_build
AMI Packer Build with GitLab CI/CD Pipelin

Build Golden AMIs with Packer and AWS CodePipeline

Written by Hendrik Hagen

    Architecture and Workflow
    Building the Pipeline
    Workflow Test
        Push Packer Configuration
        Build AMI with Packer
        Security Scan
        Share AMI
    Summary

When leveraging AWS services such as EC2, ECS, or EKS, achieving standardized and automated image creation and configuration is essential for securely managing workloads at scale. The concept of a Golden AMI is often used in this context. Golden AMIs represent pre-configured, hardened and thoroughly tested machine images that encompass a fully configured operating system, essential software packages, and customizations tailored for specific workload. It is also strongly recommended to conduct comprehensive security scans during the image creation process to mitigate the risk of vulnerabilities.

By adopting Golden AMIs, you can ensure consitent configuration across different environments, leading to decreased setup and deployment times, fewer configuration errors, and a diminished risk of security breaches.

In this blog post, I would like to demonstrate how you can leverage AWS CodePipeline and AWS Stepfunctions, along with Terraform and Packer, to establish a fully automated pipeline for creating Golden AMIs.
Architecture and Workflow

I would like to start by introducing the infrastructure that we are going to deploy as part of this blog post. The architecture diagram below provides a high-level snapshot of the components and workflow we are about to implement. Our objective is to build a CodePipeline complemented by two Stepfunctions to orchestrate the Golden AMI creation process.


![image](https://github.com/user-attachments/assets/d560b67b-dd56-4876-898f-c46ee1c95210)

# AWS Governance and Golden AMI Creation Pipeline

This repository demonstrates how to use **AWS Control Tower**, **AWS Organizations**, and other AWS services to set up a secure, multi-account environment while leveraging **Packer**, **AWS CodePipeline**, **Step Functions**, and **Terraform** to build Golden AMIs. The pipeline ensures consistent, hardened AMIs across environments with automated compliance checks.

## Overview

This project encompasses two primary objectives:

1. **Governance and Security**:
   - Set up a **multi-account AWS environment** using AWS Control Tower with governance blueprints, organizational units, and Account Factory.
   - Incorporate compliance and security services like **AWS Config**, **GuardDuty**, **CloudTrail**, and **S3 logging**.

2. **Golden AMI Creation**:
   - Automate the creation of pre-configured, hardened Golden AMIs using **Packer** and **AWS CodePipeline**.
   - Include security scans, configuration validation, and environment-specific customizations.

---

## Architecture and Workflow

### Governance with AWS Control Tower
1. **AWS Control Tower**:
   - Deploy the **Landing Zone** for automating multi-account setup with guardrails and governance policies.
   - Define **Organizational Units (OUs)** for segregating accounts into:
     - **Production**
     - **Development**
     - **Reserved** (e.g., for testing or special projects)
   - Use **Account Factory** to provision and manage AWS accounts consistently.

2. **Compliance and Security**:
   - **GuardDuty**: Detect threats and anomalous behavior across AWS accounts.
   - **AWS Config**: Monitor and evaluate configurations for compliance.
   - **CloudTrail**: Capture and log all API calls for auditing and governance.
   - **S3 Logs**: Store CloudTrail logs securely in Amazon S3 for long-term auditability.

### Golden AMI Pipeline
1. **Golden AMIs**:
   - **What are they?** Pre-configured, hardened AMIs with a baseline OS, software, and security customizations.
   - **Why use them?**
     - Ensure consistent configuration across environments.
     - Reduce deployment times and minimize security risks.

2. **Pipeline Components**:
   - **Terraform**:
     - Define infrastructure as code for AWS resources required by the pipeline.
   - **AWS CodePipeline**:
     - Orchestrate the AMI creation process across multiple stages.
   - **AWS Step Functions**:
     - Manage workflows like AMI sharing, compliance validation, and custom actions.
   - **Packer**:
     - Build and configure the Golden AMI.

3. **Workflow**:
   - **Push Packer Configuration**: Developers push configurations to a version control repository (e.g., Git).
   - **Build AMI**: Packer creates a new AMI with all required customizations.
   - **Security Scan**: Validate the AMI using tools like Amazon Inspector or custom scripts.
   - **Share AMI**: The final AMI is shared with relevant AWS accounts or OUs.

---

## Build the Pipeline: End-to-End Workflow

1. **Governance Setup**:
   - Deploy **AWS Control Tower** and create a **Landing Zone**.
   - Configure organizational units (OUs) for **Production**, **Development**, and **Reserved** accounts.
   - Enable security services:
     - **GuardDuty** for threat detection.
     - **AWS Config** for compliance monitoring.
     - **CloudTrail** for API logging.

2. **Pipeline Setup**:
   - Use **Terraform** to provision AWS CodePipeline, Step Functions, and supporting infrastructure.
   - Configure **Packer** to build AMIs dynamically based on environment-specific variables.
   - Add a Python script (`packer_template.py`) to generate dynamic Packer templates.

3. **Hello World Application**:
   - Include the following provisioner in the Packer template to deploy a simple "Hello, World!" application:
     ```bash
     echo "Hello, World!" > /var/www/html/index.html
     sudo service apache2 start
     ```

4. **Golden AMI Workflow Test**:
   - Push the updated Packer template to the repository.
   - Run the CodePipeline to build, validate, and share the AMI.

---

## Sample GitLab CI/CD Pipeline

Here’s an example `.gitlab-ci.yml` to integrate the Golden AMI creation process with GitLab CI/CD:

```yaml
stages:
  - build
  - scan
  - share

build-ami:
  stage: build
  script:
    # Generate Packer template using Python
    - python packer_template.py
    # Build the AMI using Packer
    - packer build packer_template.json
  artifacts:
    paths:
      - packer_template.json

scan-security:
  stage: scan
  script:
    # Run security checks (e.g., Amazon Inspector)
    - echo "Running security scans on the AMI..."
    - ./security-scan.sh

share-ami:
  stage: share
  script:
    # Share AMI with target AWS accounts
    - aws ec2 modify-image-attribute --image-id $AMI_ID --launch-permission "{\"Add\": [{\"AccountId\": \"123456789012\"}]}"



Summary

This project provides a robust and scalable solution for managing AWS accounts and creating Golden AMIs using AWS services and automation tools. By leveraging AWS Control Tower for governance and Packer with AWS CodePipeline, you can:

    Ensure secure and compliant AWS account management.

    Achieve consistent, automated image creation for EC2, ECS, and EKS workloads.

    Streamline application deployment with pre-configured AMIs.

Written by Michael W. Williams.


This detailed `README.md` file consolidates all the requested information into a cohesive document, including governance, security services, Golden AMI creation, and pipeline setup. Let me know if you'd like further refinements!

---

Below is the Python script (packer_template.py) that generates a dynamic Packer JSON template for building a custom AMI. The output of this script will be the JSON file that Packer uses to build the AMI.

Python Script: packer_template.py

----

Example JSON Output: packer_template.json
{
    "builders": [
        {
            "type": "amazon-ebs",
            "ami_name": "my-custom-ami",
            "instance_type": "t2.micro",
            "region": "us-west-2",
            "source_ami_filter": {
                "filters": {
                    "name": "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*",
                    "root-device-type": "ebs",
                    "virtualization-type": "hvm"
                },
                "most_recent": true,
                "owners": ["099720109477"]
            },
            "ssh_username": "ubuntu",
            "subnet_id": "subnet-abc123"
        }
    ],
    "provisioners": [
        {
            "type": "shell",
            "inline": [
                "echo 'Starting application installation...'",
                "echo 'Hello, World!' > /var/www/html/index.html",
                "sudo apt update && sudo apt install -y apache2",
                "sudo systemctl start apache2",
                "echo 'Application setup complete!'"
            ]
        }
    ]
}
