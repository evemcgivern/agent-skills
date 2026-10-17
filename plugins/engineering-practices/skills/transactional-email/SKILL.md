---
name: transactional-email
description: Set up and audit transactional email for a web app — provider choice (Resend or Postmark), SPF/DKIM/DMARC with verification commands, templates in code, deliverability testing, the transactional-vs-marketing compliance line, and unsubscribe handling. Use when asked to "set up email", "why are our emails going to spam", "add a new email template", "configure DKIM/DMARC", or "audit our email deliverability".
---

# Transactional Email

## Overview
Covers the email infrastructure that sits underneath account creation, password resets, billing receipts, and product notifications in a web app. Deliverability failures (landing in spam) are often invisible until a customer complains they "never got" a password reset — this skill front-loads the DNS and provider setup that prevents that, plus the compliance line between transactional and marketing email that a lot of small teams blur without meaning to.

## Provider Selection

- **Resend**: developer-first, React-Email template support (JSX templates render to HTML), good fit if the team wants templates to live as React components alongside the rest of the Next.js codebase. Strong choice for a small team already working in React.
- **Postmark**: mature deliverability reputation, separate transactional and broadcast message streams built into the product (this enforces the transactional-vs-marketing line structurally, not just by convention), detailed bounce/spam-complaint webhooks.
- Default recommendation for a small team already in Next.js/React: Resend, for template-as-code simplicity — unless deliverability reputation history or Postmark's built-in stream separation is specifically needed (e.g., after a deliverability incident). Don't switch providers without cause; migrating templates and re-verifying DNS is real work.

## Workflow

1. **Domain authentication (SPF/DKIM/DMARC).** Never send from an unauthenticated domain — it's both a deliverability killer and a spoofing risk.
   - **SPF**: copy the exact records from the provider's domain page rather than writing them from memory — they differ per provider and change over time. Resend has typically placed SPF on a `send` subdomain (an MX record plus a TXT record including Amazon SES); use the exact records the provider's dashboard shows. Postmark no longer asks you to add an include to your root SPF record; its custom Return-Path CNAME (pointing at `pm.mtasv.net`) handles SPF alignment. Wherever you do edit a domain's SPF record (e.g., the root record for Google Workspace), keep exactly one record per name and merge includes into it — multiple SPF TXT records on the same name break validation — and stay under SPF's limit of 10 DNS lookups.
   - **DKIM**: add the CNAME/TXT records the provider gives you during domain verification (Resend uses a TXT record at `resend._domainkey`; other providers use their own selectors).
   - **DMARC**: add a `_dmarc` TXT record, start at `p=none` with `rua=` reporting to an address you monitor, move to `p=quarantine` then `p=reject` only after confirming legitimate mail passes (a `p=reject` set too early can silently drop your own transactional email if SPF/DKIM aren't fully propagated yet). Gmail and Yahoo require bulk senders to publish a DMARC record; `p=none` satisfies that.
   - **Verification commands** (run after DNS changes, allow propagation time):
     ```
     dig TXT yourdomain.com | grep spf
     dig TXT send.yourdomain.com                  # Resend's SPF subdomain, if your dashboard uses it
     dig TXT resend._domainkey.yourdomain.com     # or the provider-specific DKIM selector (CNAME for some providers)
     dig TXT _dmarc.yourdomain.com
     ```
     Also use the provider's own domain-verification dashboard check — DNS propagation can lag `dig` results seen from one resolver.

2. **Template management in code.** Templates live as versioned files in the repo (React-Email JSX components for Resend, or Postmark's template API synced from a `templates/` directory) — never edited ad hoc in a provider's web dashboard, which drifts from source control and leaves no diff history. Each template gets a stable identifier used in code (`sendEmail({ template: 'password-reset', ... })`) so a template rename doesn't require touching every call site.

3. **Deliverability testing** before shipping a new template or provider change:
   - Send test emails to seed addresses across major providers (Gmail, Outlook/Microsoft, a Yahoo or iCloud address) and check spam-folder placement, not just successful delivery.
   - Check spam score via a tool like mail-tester.com or the provider's built-in preview/spam-check feature before a template goes live.
   - Verify rendering across at least Gmail web, Gmail mobile, and Outlook — email HTML/CSS support is notoriously inconsistent; a template that looks right in a browser preview can break in Outlook's rendering engine.

4. **Transactional vs. marketing compliance line.** This distinction has real compliance weight (CAN-SPAM, GDPR consent basis differ):
   - **Transactional**: triggered by a user action, required for service delivery — password reset, billing receipt, account verification, security alert. No opt-in/unsubscribe required (can't opt out of your own password reset), but must still identify the sending company clearly.
   - **Marketing**: product announcements, newsletters, re-engagement campaigns. Requires opt-in consent (or falls under legitimate interest with an easy opt-out, depending on jurisdiction) and a working unsubscribe link on every send.
   - The common mistake: sliding a marketing message into a transactional template ("your receipt, and by the way check out our new feature!") — if the promotional content is substantial, it needs its own opt-in-respecting send, not a hitchhike on a transactional email exempt from unsubscribe requirements.
   - If using Postmark, use its separate transactional/broadcast message streams to enforce this structurally; if using Resend, keep marketing on its separate broadcast/audience features or maintain the distinction by convention (separate template categories, a suppression-list check before any marketing send).

5. **Unsubscribe handling** (marketing email only, but build the plumbing correctly regardless):
   - One-click unsubscribe in every marketing send, honored promptly (no "are you sure" friction, no login-required step). Gmail and Yahoo require bulk senders (roughly 5,000+ messages a day to their users) to support RFC 8058 one-click unsubscribe via the `List-Unsubscribe` and `List-Unsubscribe-Post` headers and to honor requests within about two days; keep a visible unsubscribe link in the body too. CAN-SPAM separately allows at most 10 business days. Check the current sender guidelines before relying on exact thresholds.
   - Maintain a suppression list checked before every marketing send (even if the provider maintains one, keep an internal record for the app's own send logic to respect, especially if switching providers later).
   - Transactional email doesn't need an unsubscribe link but should still have a way for a user to stop specific non-essential ones (e.g., a "notify me when someone comments" toggle in account settings) — that's a preference setting, not a legal unsubscribe requirement.

## Checklist
- [ ] SPF/DKIM/DMARC all verified via `dig` and the provider's dashboard, not assumed from setup completion
- [ ] Templates live as code in the repo, not edited only in a provider dashboard
- [ ] New/changed templates tested across major inbox providers for spam placement and rendering
- [ ] Transactional vs. marketing classification checked for every new email type
- [ ] Marketing sends have working one-click unsubscribe honored immediately; suppression list maintained
- [ ] DMARC policy staged (`none` → `quarantine` → `reject`) rather than jumping straight to `reject`

## Output
DNS record changes needed (with verification command output), the template file(s) added/changed, and a deliverability test summary (spam score, rendering check results per provider).

## Stop Conditions
- DMARC is set to `p=reject` before SPF/DKIM have been confirmed fully propagated and passing → don't apply `p=reject` yet; this can silently drop the team's own transactional email (password resets, receipts) with no visible error on the sending side.
- A requested email blurs the transactional/marketing line (promotional content riding on a transactional trigger) → flag it rather than sending; this has real compliance exposure, not just a style preference.
- Domain DNS changes are needed but the team doesn't control the registrar/DNS provider directly → confirm access and change window before proposing a cutover, since a bad SPF/DKIM record can break all outbound mail for the domain, not just the new provider's.
