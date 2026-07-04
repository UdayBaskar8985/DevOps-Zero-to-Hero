# Day 23 - Introduction to Containers

## Why Containers?

Before containers, applications were deployed directly on servers or inside Virtual Machines.

Problems:
- Dependency conflicts
- Different library versions
- Different runtime versions
- "Works on my machine" issue
- Difficult deployments
- Poor resource utilization

---

## What is a Container?

A Container is a lightweight package that contains:
- Application Code
- Runtime
- Libraries
- Dependencies
- Configuration

It ensures the application runs consistently across different environments.

---

## Why do we need Containers?

Containers solve:
- Environment inconsistency
- Dependency management
- Faster deployments
- Better portability
- Easy scaling

---

## Traditional Deployment

Hardware
↓
Operating System
↓
Application
↓
Dependencies

Problem:
Installing multiple applications on the same server causes dependency conflicts.

Example:

Application A
- Python 3.8

Application B
- Python 3.12

Both cannot easily coexist without conflicts.

---

## Virtual Machines (VMs)

Architecture:

Hardware
↓
Hypervisor
↓
VM1 (Guest OS + App)
VM2 (Guest OS + App)
VM3 (Guest OS + App)

### Advantages

- Strong isolation
- Independent Operating System
- Better security

### Disadvantages

- Heavy
- Large storage
- High RAM usage
- Slow startup
- Multiple Guest OS

---

## Containers

Architecture:

Hardware
↓
Host Operating System
↓
Container Runtime (Docker)
↓
Container 1
Container 2
Container 3

Containers share the Host OS Kernel.

No Guest Operating System is required.

---

## Virtual Machine vs Container

| Virtual Machine | Container |
|-----------------|-----------|
| Guest OS required | No Guest OS |
| Heavy | Lightweight |
| Large image size | Small image size |
| Starts in minutes | Starts in seconds |
| High memory usage | Low memory usage |
| Uses Hypervisor | Uses Container Runtime |

---

## Container Runtime

Container Runtime is software that creates and manages containers.

Examples:
- Docker
- containerd
- CRI-O
- Podman

---

## What is Docker?

Docker is a Container Platform used to:

- Build Images
- Run Containers
- Share Images
- Manage Containers

---

## Docker Image

A Docker Image is a blueprint/template.

It contains:
- Operating System files
- Application
- Dependencies
- Libraries

Image is Read-Only.

---

## Docker Container

A Running Instance of a Docker Image.

Image
↓
docker run
↓
Container

---

## Benefits of Containers

- Lightweight
- Portable
- Faster Startup
- Better Resource Utilization
- Easy Deployment
- Easy Scaling
- Consistent Environment
- DevOps Friendly

---

## "Works on My Machine" Problem

Developer Machine
↓
Python 3.11

Production
↓
Python 3.8

Application fails.

Containers package all dependencies, eliminating this issue.

---

## DevOps Workflow

Developer
↓
GitHub
↓
CI/CD (Jenkins)
↓
Docker Image
↓
Container Registry
↓
Kubernetes
↓
Production

---

## Key Takeaways

- Containers package applications with all dependencies.
- Containers share the Host OS Kernel.
- Containers are much lighter than Virtual Machines.
- Docker is the most popular Container Platform.
- Image = Blueprint.
- Container = Running Image.
- Containers solve dependency and environment consistency problems.
```
