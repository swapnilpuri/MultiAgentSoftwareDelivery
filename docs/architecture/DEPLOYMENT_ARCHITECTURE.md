# Deployment architecture

Approved M0: web and project service have separate build contexts, Dockerfiles, independent image tags and CI. Compose in masd-infrastructure coordinates them on edge/internal service networks. Host ports bind to loopback; containers run as nonroot with a read-only root filesystem, dropped capabilities and writable temporary storage. Healthchecks live in each image; web waits for project readiness. Configuration supports ports, origins, image references and API base URL. No cloud resources are provisioned.

Infrastructure may build sibling contexts for local convenience or deploy prebuilt images with `docker compose up -d --no-build --wait`. A web compilation never consumes project source; the backend image never consumes web source. A targeted `docker compose up -d --no-deps --build project-service` should update only that artifact; verify image IDs before/after and preserve evidence. Configuration alone is not runtime proof.

Future: registry-pinned image digests, Kubernetes, Terraform/OpenTofu modules, cloud/region selection and promotion approvals. Database migrations and rollout policies require their first use case and approval. Production identity, ingress TLS, secrets, audit storage and network policy remain open deployment gates. M0 is not approved for external production access.

The Project Service uses a separate api-access bridge for its loopback diagnostic port; service-to-service traffic uses the internal service network. The web edge bridge is separate.
