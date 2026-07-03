# Day 16: Infrastructure as Code (IaC) with Terraform

## Overview
Infrastructure as Code (IaC) is the practice of provisioning and managing infrastructure using code instead of manual processes. This session explains the evolution of infrastructure automation, the limitations of vendor-specific tools, and why **Terraform** has become the industry standard for multi-cloud infrastructure management.

---

# 1. The Problem: Vendor-Specific Infrastructure Automation

Before Terraform, every cloud provider had its own Infrastructure as Code (IaC) tool. Although these tools automated infrastructure creation, they introduced **vendor lock-in**.

## Common Vendor-Specific IaC Tools

| Cloud Provider | IaC Tool |
|---------------|----------|
| AWS | CloudFormation (CFT) |
| Microsoft Azure | Azure Resource Manager (ARM) Templates |
| OpenStack | Heat Templates |

## Challenges

### Vendor Lock-in
- CloudFormation templates work only on AWS.
- ARM templates work only on Azure.
- Heat templates work only on OpenStack.

### Migration Effort
Moving infrastructure from one cloud provider to another requires rewriting infrastructure definitions.

Example:
- AWS → Azure
- CloudFormation → ARM Templates

### Technical Debt
Maintaining multiple Infrastructure as Code tools increases:
- Complexity
- Maintenance effort
- Learning curve

### Hybrid & Multi-Cloud Challenges

Many organizations use multiple cloud providers simultaneously.

Example:
- AWS → Compute & Storage
- Azure → DevOps & Identity
- GCP → AI & Machine Learning

Without a common IaC tool, engineers must maintain different automation scripts for each platform.

---

# 2. The Solution: Terraform

Terraform is an Infrastructure as Code tool developed by **HashiCorp**.

It provides a single language to provision infrastructure across multiple cloud providers.

## Advantages

### Universal Tool
Instead of learning multiple cloud-specific IaC tools, learn one tool:

- AWS
- Azure
- Google Cloud Platform (GCP)
- DigitalOcean
- VMware
- Kubernetes
- Many more

### Provider-Based Architecture

Terraform communicates with cloud providers using **Providers**.

Examples:
- AWS Provider
- Azure Provider
- Google Provider
- Kubernetes Provider

### Easier Migration

When changing cloud providers, you usually only update:
- Provider configuration
- Resource definitions (where services differ)

The Terraform workflow remains the same.

### Consistent Workflow

```
Write Terraform Code
        ↓
terraform init
        ↓
terraform plan
        ↓
terraform apply
```

---

# 3. Core Concept: Infrastructure Through APIs

Terraform works by communicating with cloud providers using APIs.

## What is an API?

An **Application Programming Interface (API)** allows one software application to communicate with another.

Instead of manually creating resources through a web console, Terraform sends API requests automatically.

---

## How Terraform Uses APIs

Step 1:
Write infrastructure in Terraform (HCL).

Example:

```hcl
resource "aws_instance" "web" {
    ...
}
```

Step 2:
Terraform identifies the configured Provider.

Step 3:
The Provider converts Terraform code into cloud-specific API requests.

Step 4:
The cloud provider creates the requested infrastructure.

Step 5:
Terraform records the infrastructure state in the **terraform.tfstate** file.

---

## Terraform Architecture

```
DevOps Engineer
        │
        ▼
Terraform Configuration (HCL)
        │
        ▼
Terraform Provider
        │
        ▼
Cloud Provider API
        │
        ▼
Infrastructure Created
```

---

# 4. Important Interview Definitions

## Infrastructure as Code (IaC)

Infrastructure as Code (IaC) is the practice of provisioning and managing infrastructure using code instead of manual processes.

Examples:
- Terraform
- AWS CloudFormation
- Azure ARM Templates
- OpenStack Heat Templates

### Benefits

- Automation
- Consistency
- Version Control
- Repeatability
- Reduced Human Error

---

## Terraform

Terraform is a cloud-agnostic Infrastructure as Code tool that uses Providers to provision and manage infrastructure across multiple cloud platforms.

---

## Provider

A Provider is a plugin that allows Terraform to communicate with a specific platform.

Examples:
- AWS Provider
- Azure Provider
- Google Provider
- Kubernetes Provider
- Docker Provider

---

## API

An API (Application Programming Interface) allows software systems to communicate with each other.

Terraform uses APIs to:
- Create resources
- Update resources
- Delete resources
- Retrieve infrastructure information

---

# 5. Why Terraform Became the Industry Standard

Terraform is widely used because it provides:

- Multi-cloud support
- Hybrid cloud support
- Declarative Infrastructure as Code
- Large provider ecosystem
- Consistent workflow
- Easy CI/CD integration
- Strong community support

---

# Section Summary

Before Terraform, engineers had to learn multiple vendor-specific Infrastructure as Code tools.

Terraform solves this problem by providing:

- One declarative language (HCL)
- Provider-based architecture
- Multi-cloud support
- Consistent workflow

Instead of learning many cloud-specific tools, DevOps engineers learn Terraform once and apply the same concepts across different cloud platforms.

---

# Study Tasks (2 Hours)

## Task 1: Draw the Architecture

```
DevOps Engineer
        │
        ▼
Terraform
        │
        ▼
Providers
        │
        ├── AWS
        ├── Azure
        ├── GCP
        └── Kubernetes
```

---

## Task 2: Learn HTTP API Methods

| Method | Purpose |
|----------|----------|
| GET | Retrieve information |
| POST | Create a resource |
| PUT | Update or replace a resource |
| DELETE | Remove a resource |

Terraform Providers internally use these API operations when communicating with cloud platforms.

---

## Task 3: Prepare for Hands-on Practice

Before the next session:

- Install Terraform
- Install AWS CLI
- Configure AWS Credentials
- Verify AWS Account Access
- Prepare to create your first EC2 instance using Terraform

---

# Interview Question

### Q: What is the difference between Terraform and CloudFormation?

**Terraform**
- Cloud-agnostic
- Supports multiple cloud providers
- Uses Providers
- Same workflow across clouds

**CloudFormation**
- AWS-specific
- Works only within AWS
- Cannot provision resources on other cloud platforms
