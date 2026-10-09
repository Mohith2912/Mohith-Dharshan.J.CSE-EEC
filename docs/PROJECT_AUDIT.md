# Portfolio audit

## Content review

- Identity, contact details, education, academic results, experience, and core skills were checked against `Mohith_Dharshan_Resume.pdf`.
- The GitHub profile and all 31 public repository records were reviewed on 9 October 2026.
- Featured project explanations were prepared from repository READMEs, manifests, directory structures, and core service boundaries.
- Portfolio authorship is consistently presented as Mohith Dharshan J.
- Experimental or prototype behavior is described as such; the copy does not claim that unintegrated models or external services are production features.

## Experience architecture

The site is deliberately static: semantic HTML provides the complete reading order, CSS supplies the visual system and responsive layout, and two small JavaScript files provide content rendering, filtering, progressive reveal, navigation state, and the native project dialog. There is no runtime API, database, analytics tracker, or secret.

## Visual direction

The interface takes high-level cues from the supplied KRATOS reference—dark atmosphere, concentrated red accents, bold typography, restrained glow, and cinematic pacing—while using an original layout, identity system, project narrative, and interaction model for Mohith’s work.

The academic chapter takes high-level cues from the supplied Mrithula Vijay reference—generous section rhythm, editorial italic emphasis, compact navigation, and bordered interest cards—then translates them into Mohith’s palette and content. Descriptions remain visible rather than relying on hover.

## Accessibility and resilience

- Semantic landmarks, heading order, visible labels, keyboard-operable native controls, and descriptive link/button names.
- Strong focus indicators, 44px minimum interactive targets, high-contrast dark surfaces, and a high-contrast preference override.
- Reduced-motion support disables decorative animation and reveals all content immediately.
- Mobile navigation exposes accurate expanded state; the project overlay uses the native dialog element.
- The repository atlas remains readable when JavaScript content filters return no results.

## Verification

- Automated integrity check: 7 featured case studies, 30 unique project repository records, and all required assets. The GitHub profile README is intentionally kept separate.
- JavaScript syntax checked with Node.js.
- Desktop viewport reviewed at 1265 × 708.
- Mobile viewport reviewed at 390 × 844.
- Mobile navigation, project dialog, and repository search exercised in the browser.
- Resume source and committed PDF blob hashes match exactly.

## Deployment

The root directory is the public site. `vercel.json` adds clean URLs and conservative security headers. No build command is required.
