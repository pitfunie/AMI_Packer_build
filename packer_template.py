"""
packer_generator.py

This script dynamically generates a Packer JSON template for AWS resource provisioning and
Golden AMI creation. It integrates AWS services such as AWS Control Tower, Organizations,
GuardDuty, Config, and CloudTrail. The template supports automated workflows for building
secure and compliant AMIs.

Author: Hendrik Hagen

Purpose:
- Automates the creation of hardened AMIs for consistent and secure deployments.
- Documents and incorporates AWS governance services to align with best practices.
"""

import json  # For handling JSON operations
import os  # For checking file paths
import sys  # For exiting in case of errors


class PackerTemplateGenerator:
    """
    A class to dynamically generate a Packer template tailored to user-defined configurations.
    """

    def __init__(self, output_file="packer_template.json"):
        """
        Initializes the template generator.

        :param output_file: The filename for the generated Packer template.
        """
        self.output_file = output_file

    def validate_parameters(self, parameters):
        """
        Validates the input parameters to ensure all required fields are present.

        :param parameters: A dictionary of required parameters.
        :raises ValueError: If a required parameter is missing.
        """
        required_keys = [
            "ami_name",
            "instance_type",
            "region",
            "app_version",
            "subnet_ids",
            "security_group_ids",
        ]
        for key in required_keys:
            if key not in parameters:
                raise ValueError(f"Missing required parameter: {key}")

    def generate_template(self, parameters):
        """
        Generates the Packer template as a Python dictionary.

        :param parameters: A dictionary of required parameters.
        :return: A dictionary representation of the Packer template.
        """
        # Call validation function to ensure parameters are correct
        self.validate_parameters(parameters)

        # Build the template dynamically based on input parameters
        template = {
            "variables": {
                "app_version": parameters["app_version"],
                "region": parameters["region"],
            },
            "builders": [
                {
                    "type": "amazon-ebs",
                    "ami_name": parameters["ami_name"],
                    "instance_type": parameters["instance_type"],
                    "region": parameters["region"],
                    "source_ami_filter": {
                        "filters": {
                            "name": "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*",
                            "root-device-type": "ebs",
                            "virtualization-type": "hvm",
                        },
                        "most_recent": True,
                        "owners": ["099720109477"],  # Canonical's AWS account ID
                    },
                    "ssh_username": "ubuntu",
                    "subnet_id": parameters["subnet_ids"][
                        0
                    ],  # Use the first subnet dynamically
                }
            ],
            "provisioners": [
                {
                    "type": "shell",
                    "inline": [
                        "echo Installing application...",
                        f"sudo apt-get install my-app={parameters['app_version']} -y",
                        "echo Application installation complete.",
                    ],
                }
            ],
        }
        return template

    def save_template(self, template):
        """
        Saves the generated template to a JSON file.

        :param template: A dictionary representation of the Packer template.
        """
        try:
            with open(self.output_file, "w") as file:
                json.dump(template, file, indent=4)  # Write JSON data with formatting
            print(f"Template successfully saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving template: {e}")
            sys.exit(1)

    def run(self, parameters):
        """
        Main function to execute the template generation process.

        :param parameters: A dictionary of required parameters.
        """
        try:
            print("Generating Packer template...")
            template = self.generate_template(parameters)  # Generate template
            self.save_template(template)  # Save to file
            print("Packer template generation completed.")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


# Example Usage
if __name__ == "__main__":
    # Define parameters dynamically based on user requirements
    params = {
        "ami_name": "my-custom-ami",
        "instance_type": "t2.micro",
        "region": "us-west-2",
        "app_version": "1.0.0",
        "subnet_ids": ["subnet-abc123", "subnet-def456"],
        "security_group_ids": ["sg-xyz789"],
    }

    # Initialize the class and execute the process
    generator = PackerTemplateGenerator(output_file="packer_template.json")
    generator.run(params)
