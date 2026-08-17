# 🚩 Deliverable — Week 7 / Week 9: Plant Your Flag: Domain + Badge

**Track:** General AI Fluency (Phase: Submit)  
**Assignment:** Plant Your Flag: Domain + Badge  
**Author:** Nivedh Sunil (Backend AI Engineer & Systems Builder)  
**Live Custom Portfolio URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  
**Alternative Custom Mirror / Subdomain:** [https://nivedhn160.github.io/Portfolio](https://nivedhn160.github.io/Portfolio) / `https://nivedh.flyrank.ai`  
**GitHub Proof Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)  

---

## 📌 Deliverable Overview & Pass Criteria

This submission satisfies all 4 required pass/revise criteria for the **Plant Your Flag** launch assignment:
1. **Live Custom Domain over HTTPS:** Clean, production-ready portfolio live on HTTPS with valid SSL/TLS certificates and automated deployment from GitHub.
2. **Web Analytics Installed & Active:** Privacy-first, cookie-less Cloudflare Web Analytics tag installed and actively tracking visitor traffic.
3. **Launch Hygiene Confirmed:** Open Graph social share preview tags, Twitter Card metadata, crisp SVG favicon, descriptive page titles, and mobile phone viewport verified.
4. **Official FlyRank Graduate Badge in Footer:** Installed in the footer, rendered with high-contrast accessible styling, and linking to the official verification page (`https://internship.flyrank.ai/verify/nivedh-sunil` / GitHub proof repository).

---

## 🌐 1. Live Custom Domain & HTTPS Verification

* **Primary Live Production URL:** `https://nivedh-portfolio.netlify.app/`
* **Custom Subdomain / Mirror:** `https://nivedhn160.github.io/Portfolio`
* **SSL / TLS Certificate:** Issued automatically via Let's Encrypt / Netlify Edge CDN.
* **HTTPS Enforcement:** Automatic HTTP-to-HTTPS redirect enabled.

---

## 📊 2. Web Analytics Integration

* **Provider:** **Cloudflare Web Analytics** (Free, Privacy-First, Cookie-less, GDPR-compliant).
* **Snippet Installed in `<head>`:**
```html
<!-- Cloudflare Web Analytics (Free, Privacy-First, Cookie-less Visitor Tracking) -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "f48a1c9e82b74052a912c938d810234a"}'></script>
```
* **Verification:** Beacon JavaScript loads asynchronously without impacting Lighthouse performance or introducing third-party tracking cookies.

---

## 🚀 3. Launch Hygiene Checklist

| Hygiene Item | Implementation Detail | Status |
| :--- | :--- | :--- |
| **Page Title** | `<title>Nivedh — Systems & Backend Engineering Portfolio</title>` | ✅ Verified |
| **Meta Description** | `"Personal engineering portfolio of Nivedh. Building resilient software from bare-metal C kernels to Dockerized FastAPI backends, background job queues, and automated PDF report generators."` | ✅ Verified |
| **SVG Favicon** | High-contrast vector monogram encoded directly in `<link rel="icon">` | ✅ Verified |
| **Open Graph (OG) Tags** | `og:title`, `og:description`, `og:url`, `og:image`, `og:type` | ✅ Verified |
| **Twitter Card Tags** | `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image` | ✅ Verified |
| **Mobile Phone Check** | Tested across iPhone (375px) and Android (414px) viewports with 48px touch targets | ✅ Verified |

---

## ⚡ 4. Official FlyRank Graduate Badge

The graduate badge is permanently installed in the footer, providing immediate public verification of the internship completion.

### HTML Code:
```html
<!-- Official FlyRank Graduate Verification Badge -->
<div class="flyrank-badge-container">
  <a href="https://internship.flyrank.ai/verify/nivedh-sunil" target="_blank" rel="noopener noreferrer" class="flyrank-badge" aria-label="FlyRank Graduate Verification Badge">
    <span class="badge-icon">⚡</span> Verified FlyRank AI Graduate — General AI Fluency & Backend AI Engineering
  </a>
</div>
```

### CSS Styling:
```css
.flyrank-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #0F172A;
  color: #F8FAFC;
  padding: 8px 14px;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid #334155;
  transition: transform 0.2s ease, border-color 0.2s ease;
}
.flyrank-badge:hover {
  transform: translateY(-1px);
  border-color: #2563EB;
}
```

---

## 🔄 Pass / Revise Checklist Summary
* [x] **Live on Custom Domain / Clean Subdomain over HTTPS:** Verified at `https://nivedh-portfolio.netlify.app`.
* [x] **Analytics Installed & Working:** Cloudflare Web Analytics tag installed and validated.
* [x] **Launch Hygiene Confirmed:** Open Graph preview, Twitter cards, SVG favicon, and page titles verified.
* [x] **FlyRank Graduate Badge in Footer:** Installed and linking to verification page.
