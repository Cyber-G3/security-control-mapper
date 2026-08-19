# Security Policy

## Supported version

Security fixes are applied to the latest release and the current `main` branch.

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability that could expose users, credentials, data, or system integrity.

Report security concerns privately to the repository owner through an appropriate private contact channel. Include a concise description, affected component, reproduction steps where safe, impact, and any suggested mitigation.

## Scope

This repository contains deterministic mapping and reporting logic. It does not process production credentials by design and does not require external paid services at runtime.

## Security principles

- no secrets committed to the repository;
- least-privilege CI permissions;
- dependency auditing;
- static security analysis;
- versioned mapping data;
- explicit separation between technical evidence and compliance conclusions.
