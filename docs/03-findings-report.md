# SOX ITGC Assessment — Findings Report
### NorthStar Lending, Inc. — IPO Readiness

> **Portfolio note:** Fictional company and data; a lab exercise demonstrating a SOX
> ITGC assessment deliverable.

**Prepared by:** Salim Mbaye
**Scope:** IT General Controls supporting financial reporting (4 domains, 16 controls)
**Standard:** PCAOB AS 2201; SOX Section 404 (ICFR)
**Date:** October 2026

---

## 1. Executive summary

NorthStar Lending's IT General Controls were assessed across the four ITGC domains as
part of IPO readiness. Of **16 controls tested, 11 (69%) operated effectively**. Five
deficiencies were identified, including **one material weakness**.

| Overall conclusion | **MATERIAL WEAKNESS** |
|--------------------|------------------------|

Because a material weakness exists, **ITGC cannot currently be concluded effective**,
and the automated controls and system-generated reports that depend on these IT
controls cannot yet be fully relied upon for financial-reporting purposes. The
material weakness is concentrated in **change management** (developer access to
production), with additional significant deficiencies in **access management**.

![ITGC test results by domain](../outputs/itgc-status-by-domain.png)

## 2. Deficiencies

### CM-03 — Developers have standing production access — **Material Weakness**
- **Condition:** Developers hold standing access to deploy directly to the production
  financial systems, with no enforced separation between who writes code and who
  releases it.
- **Why it's a material weakness:** This is a **segregation-of-duties** failure over
  the systems that produce financial data. An unreviewed or unauthorized change could
  alter financial transactions or reporting with no compensating control to catch it —
  a reasonable possibility of a material misstatement that would not be prevented or
  detected.
- **Root cause:** Rapid startup growth; deployment speed prioritized over control.
- **Remediation:** Remove developer standing production access; route all deployments
  through a controlled CI/CD pipeline with independent approval and an audit trail.

### AC-03 — Terminated access not revoked timely — **Significant Deficiency**
- **Condition:** In a sample of 15 terminations, access was not revoked within the
  24-hour SLA for several separated users.
- **Impact:** Former employees may retain access to financial systems — an access and
  fraud risk.
- **Remediation:** Automate deprovisioning via an HR-triggered workflow; monitor SLA.

### AC-02 — Quarterly access recertification not consistently performed — **Significant Deficiency**
- **Condition:** Recertification evidence was missing for part of the year.
- **Impact:** Access creep — users may accumulate inappropriate access undetected.
- **Remediation:** Formalize and enforce quarterly recertification with tracked completion.

### AC-06 — Segregation-of-duties conflicts unresolved — **Control Deficiency**
- **Condition:** The SoD conflict report shows unresolved conflicting access grants.
- **Remediation:** Implement an SoD ruleset and remediate the conflicting grants.

### CO-02 — Backups not restore-tested — **Control Deficiency**
- **Condition:** Backups run, but restoration has not been periodically tested.
- **Remediation:** Establish documented periodic restore testing with retained evidence.

## 3. Remediation priority

| Priority | Control | Severity | Action |
|----------|---------|----------|--------|
| 1 | CM-03 | Material Weakness | Remove dev prod access; controlled CI/CD with approval |
| 2 | AC-03 | Significant Deficiency | Automate timely deprovisioning |
| 3 | AC-02 | Significant Deficiency | Enforce quarterly access recertification |
| 4 | AC-06 | Control Deficiency | Deploy SoD ruleset; clear conflicts |
| 5 | CO-02 | Control Deficiency | Periodic, evidenced restore testing |

The material weakness (CM-03) must be remediated and the control operating effectively
for a period before management could assert ITGC is effective. Access-domain
deficiencies cluster around identity lifecycle and are addressable with automation.

## 4. How to reproduce

```bash
pip install -r scripts/requirements.txt
python3 scripts/itgc_assessment.py
# regenerates outputs/: assessment summary + status chart
```

## 5. Standards referenced

- Sarbanes-Oxley Act of 2002, Section 404 (ICFR)
- PCAOB Auditing Standard 2201 (deficiency severity definitions)
- COSO Internal Control — Integrated Framework (control environment)
