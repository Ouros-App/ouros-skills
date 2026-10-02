# Security Policy

## Scope

This repository contains agent instructions, not production credentials or target lists.

Do not commit secrets, access tokens, private endpoints, real customer data, or exploit artifacts containing sensitive data.

## Reporting

For vulnerabilities in these skills, use private security reporting in the Ouros organization when available. If private reporting is unavailable, contact the maintainers without publishing credentials or sensitive reproduction data.

## Runtime boundary

The security skills default to **local or explicitly authorized QA environments**. They are not authorization to test third-party systems or production.

Cleanup removes test-created fixtures and restores reversible configuration. It must never erase, tamper with, or suppress security/audit logs.
