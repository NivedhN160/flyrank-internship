# 📖 FlyRank API Reference & Endpoint Catalogue

Comprehensive OpenAPI endpoint documentation across all microservices and Capstones.

---

## 📌 1. Embeddable Widget & Lead Platform (`Port 8000`)

* `GET /widget.js?id={widget_id}` — Returns embeddable JavaScript snippet.
* `POST /api/v1/leads` — Ingests and enriches customer leads with Geo-IP data.
* `GET /api/v1/widgets/{id}/config` — Retrieves widget configuration (colors, text, allowed origins).
* `GET /api/v1/dashboard/stats` — Metrics endpoint (Total submissions, active widgets, geo breakdown).

---

## 📌 2. AI Image Understanding & Content Matching (`Port 8000`)

* `POST /api/v1/batch/process-images` — Ingests images, extracts vision tags, and generates 1536-dim embeddings.
* `GET /api/v1/posts/{id}/images` — Evaluates semantic match using cosine similarity and Mismatch Guard.
* `POST /api/v1/review/approve` — Human reviewer approval endpoint.
* `POST /api/v1/review/reject` — Human reviewer rejection endpoint.
* `GET /api/v1/costs` — Attributed API cost tracking breakdown.

---

## 📌 3. LLM Usage Metering & Billing Engine (`Port 8000`)

* `POST /api/v1/meter` — Raw idempotent usage event recording.
* `POST /api/v1/generate` — Simulates billable LLM generation with automatic token metering.
* `GET /api/v1/usage?tenant_id={id}` — Retrieves monthly usage rollup and quota progress.
* `POST /api/v1/webhooks/stripe` — Verifies Stripe HMAC webhook signatures and updates tier quotas.

---

## 📌 4. Multi-Platform Social Campaign Publisher (`Port 8000`)

* `POST /api/v1/campaigns` — Creates multi-platform campaign with 1:1 and 16:9 image crops.
* `POST /api/v1/publish?campaign_id={id}` — Triggers asynchronous batch dispatch.
* `POST /webhook/social-delivery` — Webhook listener verifying delivery confirmations.
