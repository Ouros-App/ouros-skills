# Ouros security model

Load this reference only when an audit needs Ouros-specific boundaries.

## Core trust path

`client -> ms-auth-service -> Keycloak -> JWT -> protected services`

Protected services include `ms-spring-api`, `ms-ai-server`, `ms-mcp-server-ouros-knowledge`, and telemetry/dashboard surfaces.

Authorization must be enforced by the service handling the resource, not trusted solely because a previous hop authenticated the caller.

## High-value boundaries

### Identity and authorization

- JWT issuer, audience, expiry, roles, and scopes.
- Cross-user, cross-farm, and cross-enterprise isolation.
- Administrative endpoints and service-to-service credentials.

### AI and tools

- MIDAS input -> guardrail -> router/agent -> MCP -> tool -> data.
- Tool arguments are untrusted model output until server-side authorization validates them.
- Conversation/thread context must not cross authenticated principals.

### Data

- PostgreSQL roles should follow least privilege.
- Analytics/read-only identities must not silently gain mutation privileges.
- Sensitive data should not leak through logs, telemetry, or model context.

### Delivery

- GitHub Actions, Infisical/secret injection, containers, and deployment credentials.
- Treat pull-request-controlled input as untrusted.

## Default audit environment

Use local or QA only unless the operator explicitly expands scope.

Create dedicated security-test principals/resources and prefix temporary state with a run identifier such as `redteam_<run-id>_`.

Never assume a resource is disposable merely because its name looks temporary. Track exact IDs created by the current run.

## Evidence policy

Preserve request/response metadata needed to reproduce, relevant logs and trace IDs, affected code/config references, and exact test identity/resource relationships.

Redact credentials and unnecessary personal data. Cleanup test-created state after evidence is captured. Do not delete audit logs.
