# IshemaLink API

Backend API for domestic + international logistics workflows in Rwanda.

## Features implemented (rubric-aligned)
- Modular apps with explicit **payments** domain: `core`, `domestic`, `international`, `payments`, `identity`, `pricing`, `privacy`, `rbac`, `gov`, `analytics`, `notifications`.
- Health endpoints: `GET /api/` and `GET /api/status/` plus deep check `GET /api/health/deep/`.
- Custom user model with Rwanda phone and NID validation.
- Identity flow with OTP simulation (cache-backed).
- Hybrid auth entry points (session + JWT).
- Shipment status updates with async `await` notification simulation and tracking logs.
- Tariff caching with invalidation endpoint and cache headers.
- Paginated shipment listing with search/filter support.
- Payment workflow endpoints for MoMo initiation and webhook callbacks.
- OpenAPI schema/docs wiring via drf-spectacular.
- Docker-ready setup.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ishemalink_api/manage.py migrate
python ishemalink_api/manage.py runserver
```

## Key endpoints required by rubric
- `GET /api/status/`
- `GET /api/`
- `POST /api/auth/register/`
- `POST /api/auth/verify-nid/`
- `GET /api/users/me/`
- `POST /api/users/agents/onboard/`
- `POST /api/shipments/create/`
- `POST /api/shipments/{id}/update-status/`
- `POST /api/shipments/batch-update/`
- `GET /api/shipments/{id}/tracking/`
- `GET /api/shipments/?page=1&size=20`
- `GET /api/pricing/tariffs/`
- `POST /api/pricing/calculate/`
- `POST /api/admin/cache/clear-tariffs/`
- `POST /api/payments/initiate/`
- `POST /api/payments/webhook/`
- `GET /api/shipments/tracking/{tracking_code}/live/`
- `POST /api/notifications/broadcast/`
- `GET /api/admin/dashboard/summary/`

## Reflection (300+ words)
The line between domestic and international logistics is not just technical, it is operational. In this project I separated those concerns into dedicated Django apps so that each flow could evolve without breaking the other. Domestic deliveries in Rwanda rely on speed and simplicity: shorter forms, fewer customs constraints, and optimization for mobile-first agents working with unstable connectivity. International shipments, by contrast, require customs-specific identifiers such as TIN/passport, traceability across borders, and stricter compliance gates before movement.

The key design choice was to keep both flows under one API contract while isolating business logic. I kept shared identity and validation in `core`, pricing intelligence in `pricing`, shipment execution in `domestic`, and payment processing in `payments`. This made it possible to reuse key security and governance controls (authentication, audit logs, permissions) while preserving domain boundaries.

For local context, Rwanda-specific KYC requirements are first-class: phone numbers are normalized around the `+2507XXXXXXXX` pattern and NID format checks are centralized, typed, and testable. This reduces duplicate logic and makes audits easier. In addition, caching tariffs in memory with explicit invalidation balances performance and control. Agents need fast responses in districts where connectivity can degrade, and cached rate cards prevent repeated database lookups from becoming a bottleneck.

On the reliability side, asynchronous status processing allows shipment updates to proceed while SMS/email side effects run independently. In practical terms, a temporary notification gateway issue should not block a status transition. I also added paginated responses with metadata so low-end devices can operate safely at scale.

Overall, the architecture keeps domestic and international concerns separate, but integrates them through consistent interfaces, shared security posture, and clear operational observability. That balance is what makes the platform practical for Rwanda’s mixed terrain, device diversity, and compliance reality.
