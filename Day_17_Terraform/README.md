# Day 17 — Launch an EC2 Instance with Terraform

This guide walks through provisioning a single AWS EC2 instance using Terraform: setting up an IAM user, configuring the AWS CLI, writing provider/resource configuration, and running the core Terraform workflow (`init` → `plan` → `apply` → `destroy`).

---

## Step 1: Create a Terraform Project

```bash
cd ~/DevOps-Zero-to-Hero/Day17_Terraform/Terraform

touch main.tf provider.tf variables.tf outputs.tf

ls
```

Expected output:

```
main.tf
outputs.tf
provider.tf
variables.tf
```

---

## Step 2: Create an IAM User for Terraform

In the AWS Console:

1. Open **IAM**.
2. Go to **Users**.
3. Click **Create user**.
4. User name: `terraform-user`
5. Click **Next**.
6. Attach the policy: `AdministratorAccess`

   > For learning, this is acceptable. In production, use least-privilege permissions.
7. Create the user.

---

## Step 3: Create Access Keys

1. Open the `terraform-user`.
2. Go to **Security credentials**.
3. Under **Access keys**, click **Create access key**.
4. Select **Command Line Interface (CLI)**.
5. Create the key.
6. Copy the **Access Key ID** and **Secret Access Key**.

---

## Step 4: Configure the AWS CLI

```bash
aws configure
```

```
AWS Access Key ID: <your-access-key-id>
AWS Secret Access Key: <your-secret-access-key>
Default region name: eu-central-1
Default output format: json
```

Verify:

```bash
aws sts get-caller-identity
```

Expected output:

```json
{
  "UserId": "...",
  "Account": "...",
  "Arn": "..."
}
```

---

## Step 5: Write the Provider Configuration

`provider.tf`:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  required_version = ">= 1.5"
}

provider "aws" {
  region = "eu-central-1"
}
```

---

## Step 6: Create `main.tf`

### Option A — Static AMI (example only)

```hcl
resource "aws_instance" "my_server" {
  ami           = "ami-02003f9f0fde924ea"
  instance_type = "t2.micro"

  tags = {
    Name = "Terraform-Server"
  }
}
```

> ⚠️ **Important:** AMI IDs are region-specific and change over time whenever a new image is published. A hardcoded ID will eventually go stale or fail if you switch regions. Option B below fixes this by always resolving the latest Ubuntu 24.04 LTS AMI dynamically.

### Option B — Dynamic AMI lookup (recommended)

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS account

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "my_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  tags = {
    Name = "Terraform-Server"
  }
}
```

`outputs.tf` (useful with Option B, to see which AMI/instance was created):

```hcl
output "instance_id" {
  value = aws_instance.my_server.id
}

output "instance_public_ip" {
  value = aws_instance.my_server.public_ip
}

output "ami_used" {
  value = data.aws_ami.ubuntu.id
}
```

---

## Step 7: Initialize Terraform

```bash
terraform init
```

Expected output:

```
Terraform has been successfully initialized!
```

---

## Step 8: Validate

```bash
terraform validate
```

Expected:

```
Success! The configuration is valid.
```

---

## Step 9: Format

```bash
terraform fmt
```

---

## Step 10: Preview

```bash
terraform plan
```

Terraform will show:

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

Nothing is created yet.

---

## Step 11: Apply

```bash
terraform apply
```

Terraform asks:

```
Do you want to perform these actions?
```

Type:

```
yes
```

After a few seconds:

```
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

---

## Step 12: Verify

Open the AWS Console → **EC2 → Instances**. You should see an instance named **Terraform-Server**.

---

## Step 13: Destroy

When you're finished:

```bash
terraform destroy
```

Type:

```
yes
```

The EC2 instance will be deleted.

---

## Important Commands

```bash
terraform init
terraform validate
terraform fmt
terraform plan
terraform apply
terraform destroy
terraform show
terraform state list
terraform output
```

---

## Suggested Repository Structure

```
DevOps-Zero-to-Hero/
└── Day17_Terraform/
    ├── README.md
    ├── provider.tf
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── .gitignore
    └── examples/
```

## `.gitignore`

```
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl
crash.log
terraform.tfvars
```

---

## Pushing to Your Git Repository

If your repo already exists locally and is already tracked by Git:

```bash
cd ~/DevOps-Zero-to-Hero

git add Day17_Terraform/
git commit -m "Day 17: Launch EC2 instance with Terraform"
git push
```

If this is a brand-new repo (not yet initialized or not yet connected to GitHub):

```bash
cd ~/DevOps-Zero-to-Hero

# Initialize git if this hasn't been done yet
git init

# Stage and commit
git add .
git commit -m "Day 17: Launch EC2 instance with Terraform"

# Set the default branch name
git branch -M main

# Connect to your GitHub repo (only needed once)
git remote add origin https://github.com/<your-username>/DevOps-Zero-to-Hero.git

# Push and set upstream tracking
git push -u origin main
```

> ⚠️ Double-check that `.terraform/` and `*.tfstate` files are in `.gitignore` **before** your first commit — Terraform state files can contain sensitive data (like resource IDs and, in some cases, secrets) and should never be pushed to a public repo.

If you accidentally already committed `.terraform/` or a `.tfstate` file before adding `.gitignore`, remove them from tracking (without deleting locally):

```bash
git rm -r --cached .terraform
git rm --cached terraform.tfstate terraform.tfstate.backup
git commit -m "Remove Terraform state and cache from version control"
git push
```

---

## Interview Questions & Answers

**1. What is Terraform, and what problem does it solve?**
Terraform is an open-source Infrastructure as Code (IaC) tool by HashiCorp that lets you define, provision, and manage cloud infrastructure using declarative configuration files. It solves the problem of manual, inconsistent infrastructure setup by making provisioning repeatable, versioned, and automatable.

**2. What is the difference between Terraform and other IaC tools like Ansible or CloudFormation?**
Terraform is declarative and cloud-agnostic (supports AWS, Azure, GCP, and more via providers), while CloudFormation is AWS-specific. Ansible is primarily a configuration management tool (procedural, agentless) rather than a provisioning tool, though it can do both to some extent.

**3. What is a Provider in Terraform?**
A provider is a plugin that lets Terraform interact with a specific platform's API (e.g., `hashicorp/aws`, `azurerm`, `google`). It defines the resource types and data sources available for that platform.

**4. What is the purpose of `terraform init`?**
It initializes a working directory: downloads the required provider plugins, sets up the backend for state storage, and prepares modules referenced in the configuration.

**5. What does `terraform plan` do, and why is it important?**
It creates an execution plan showing what actions Terraform will take (add/change/destroy) without actually applying them. It's a safety check to review changes before they affect real infrastructure.

**6. What is Terraform state, and why is it needed?**
The state file (`terraform.tfstate`) maps your configuration to real-world resources. Terraform uses it to know what already exists, detect drift, and calculate what changes are needed on the next plan/apply.

**7. Why shouldn't `.tfstate` files be committed to version control?**
They can contain sensitive data (resource IDs, sometimes secrets/outputs in plaintext) and are prone to merge conflicts in team settings. Best practice is to use a remote backend (e.g., S3 with DynamoDB locking) instead.

**8. What is a remote backend in Terraform, and why use one?**
A remote backend stores the state file outside the local machine (e.g., AWS S3, Terraform Cloud). It enables team collaboration, state locking to prevent concurrent modification, and better security/durability than local state.

**9. What is state locking, and why does it matter?**
State locking prevents two people or processes from running `apply` simultaneously against the same state, which could corrupt it. Backends like S3 + DynamoDB support locking.

**10. What's the difference between `terraform apply` and `terraform apply -auto-approve`?**
`terraform apply` prompts for manual confirmation ("yes") before making changes. `-auto-approve` skips that prompt, useful for CI/CD pipelines but riskier for manual runs.

**11. What is a Terraform data source, and how is it different from a resource?**
A resource creates and manages infrastructure. A data source only reads existing information (e.g., `data "aws_ami"` to fetch the latest AMI ID) without creating or modifying anything.

**12. Why is hardcoding an AMI ID a bad practice?**
AMI IDs are region-specific and change whenever a new image version is published. Hardcoding one risks referencing a deprecated or unavailable image, especially across regions. Using a `data "aws_ami"` lookup with filters keeps the configuration current automatically.

**13. What are Terraform variables, and why use `variables.tf`?**
Variables (`variable` blocks) let you parameterize configuration instead of hardcoding values, improving reusability across environments. `variables.tf` conventionally centralizes these declarations.

**14. What are Terraform outputs used for?**
`output` blocks expose values (like an instance's public IP) after apply, useful for chaining modules, feeding into scripts, or simply displaying key information (`terraform output`).

**15. What is the difference between `variables.tf` and `terraform.tfvars`?**
`variables.tf` declares variables (name, type, description, defaults). `terraform.tfvars` supplies actual values for those variables, keeping sensitive/environment-specific values separate from the logic.

**16. What does `terraform validate` check, exactly?**
It checks the syntax and internal consistency of the configuration (e.g., correct HCL syntax, valid argument names) — it does not check against actual cloud provider state or credentials.

**17. What does `terraform fmt` do?**
It rewrites configuration files into a canonical formatting style (consistent indentation and alignment), primarily for readability and consistency across a team.

**18. What happens if you run `terraform apply` twice without changing the config?**
Terraform compares the current state to the real infrastructure and configuration; if nothing has changed, it reports "No changes" and does nothing — Terraform is idempotent.

**19. What is Terraform drift, and how do you detect it?**
Drift occurs when real infrastructure changes outside of Terraform (e.g., someone manually edits a resource in the AWS Console). `terraform plan` (or `terraform refresh`) detects the difference between actual state and the state file.

**20. What is the purpose of `terraform destroy`?**
It deletes all resources tracked in the current state file/configuration. It's used to tear down infrastructure that's no longer needed, avoiding ongoing cloud costs.

**21. Why did we use an IAM user with `AdministratorAccess` in this exercise, and why is that discouraged in production?**
It simplifies setup for learning since Terraform needs a wide range of permissions to create various resource types. In production, this violates least-privilege principles and increases blast radius if credentials are compromised — a scoped IAM policy limited to only the needed actions/resources should be used instead.

**22. How does Terraform authenticate with AWS?**
Commonly via the AWS credentials configured through `aws configure` (stored in `~/.aws/credentials`), environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`), an IAM role (e.g., on an EC2 instance or CI runner), or explicit provider block credentials (not recommended for secrets).

**23. What is the `required_providers` block used for?**
It pins which providers (and version constraints) Terraform should download and use, ensuring consistent behavior across environments and preventing unexpected breaking changes from provider upgrades.

**24. What's the difference between `terraform plan` and `terraform apply` in a CI/CD pipeline context?**
`plan` is typically run on pull requests to preview changes for review (often posted as a comment), while `apply` runs after merge/approval to actually provision the infrastructure — separating review from execution.

**25. How would you manage multiple environments (dev/staging/prod) with Terraform?**
Common approaches: separate state files per environment (using workspaces or separate backend configs), directory-per-environment structures, or modules with environment-specific `.tfvars` files — avoiding a single shared state across environments to reduce risk.
