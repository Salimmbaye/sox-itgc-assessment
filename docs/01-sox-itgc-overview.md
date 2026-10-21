# SOX IT General Controls (ITGC) — Overview

> **Portfolio note:** This is a lab project using the same fictional fintech,
> *NorthStar Lending, Inc.*, introduced in the
> [risk assessment project](../../risk-assessment-fintech). NorthStar is preparing
> for an eventual IPO, which is when a private company must get its controls
> SOX-ready. All data is invented.

## 1. What SOX is and why IT cares

The **Sarbanes-Oxley Act of 2002 (SOX)** was passed after the Enron and WorldCom
accounting scandals to restore trust in public-company financial reporting. The part
that matters here is **Section 404**: company management must assess and report on
the effectiveness of its **Internal Control over Financial Reporting (ICFR)**, and
(for larger filers) the external auditor must attest to it.

Here's the link to IT: modern financial statements are produced by **IT systems** —
general ledgers, billing, loan and payment platforms, databases. If those systems
aren't controlled, the numbers they produce can't be trusted. **IT General Controls
(ITGC)** are the controls over the IT environment that give assurance the financial
applications and data are reliable. If ITGCs fail, the auditor can't rely on *any*
of the automated controls or system-generated reports that sit on top of them — so
ITGC failures have outsized consequences.

> **The one-sentence version for an interview:** "ITGCs are the foundation that lets
> auditors trust the systems producing the financial statements — if they're broken,
> nothing built on those systems can be relied upon."

## 2. The four ITGC domains

Essentially every SOX ITGC program organizes around these four domains:

| Domain | What it assures | Example controls |
|--------|-----------------|------------------|
| **Access to Programs & Data** | Only authorized, appropriate users can access financial systems and data | User provisioning approval, access reviews, timely termination, privileged-access restriction, MFA, **segregation of duties** |
| **Program Changes** | Changes to financial systems are authorized, tested, and approved before production | Change approval, testing before deployment, developer ≠ deployer separation, emergency-change review |
| **Program Development** | New financial systems are built and implemented with proper controls | SDLC approvals, data-migration validation, user acceptance testing (UAT) sign-off |
| **Computer Operations** | Systems run reliably and problems are resolved | Job scheduling and monitoring, backup execution and restore testing, incident/problem management |

## 3. Two concepts that make this a finance-crossover skill

**Segregation of Duties (SoD).** No single person should control all parts of a
transaction — e.g., the same person shouldn't be able to both *write* code and
*deploy* it to production unreviewed, or both *create* a vendor and *approve* a
payment to it. SoD failures are a classic path to fraud and a frequent source of SOX
findings. (NorthStar's finding CM-03 is an SoD gap.)

**Deficiency severity.** Not every failed control is equal. SOX classifies them by
the likelihood and magnitude of a resulting **financial misstatement**:

| Classification | Meaning |
|----------------|---------|
| **Control Deficiency** | A control doesn't operate effectively, but the impact is limited. |
| **Significant Deficiency** | Important enough to merit attention by those charged with governance (audit committee). |
| **Material Weakness** | A reasonable possibility that a **material misstatement** of the financial statements would not be prevented or detected in time. The most severe — must be disclosed. |

This severity language (straight from PCAOB Auditing Standard 2201) is what separates
an IT auditor who understands *why* a control matters from one who just checks boxes.

## 4. How this project is structured

1. **Control matrix** (`data/itgc-controls.csv`) — 16 ITGC controls across the four
   domains, each with a control objective, activity, owner, test procedure, test
   result, and deficiency severity.
2. **Assessment script** (`scripts/itgc_assessment.py`) — summarizes test results,
   counts deficiencies by severity, computes a control-effectiveness rate, and
   renders a status chart.
3. **Findings report** (`docs/03-findings-report.md`) — the deficiencies, their
   severity, root cause, and remediation, written as an audit deliverable.
