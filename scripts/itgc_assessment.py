#!/usr/bin/env python3
"""
itgc_assessment.py — summarize SOX ITGC test results and classify the control
environment.

Reads  : data/itgc-controls.csv
Writes : outputs/itgc-assessment-summary.md
         outputs/itgc-status-by-domain.png
Usage  : python3 scripts/itgc_assessment.py

Deficiency severity follows PCAOB AS 2201: Control Deficiency < Significant
Deficiency < Material Weakness. See docs/01-sox-itgc-overview.md.
"""
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "itgc-controls.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

RESULTS = ["Pass", "Exception", "Fail"]
RESULT_COLORS = {"Pass": "#2e7d32", "Exception": "#f9a825", "Fail": "#c62828"}
SEVERITY_ORDER = ["None", "Control Deficiency", "Significant Deficiency", "Material Weakness"]
DOMAINS = ["Access to Programs & Data", "Program Changes",
           "Program Development", "Computer Operations"]


def load():
    if not MATRIX.exists():
        sys.exit(f"ERROR: control matrix not found at {MATRIX}")
    return pd.read_csv(MATRIX)


def overall_conclusion(df):
    present = set(df["Deficiency_Severity"])
    if "Material Weakness" in present:
        return ("MATERIAL WEAKNESS",
                "A material weakness exists. ITGC cannot be concluded effective; the "
                "deficiency has a reasonable possibility of allowing a material "
                "misstatement and must be disclosed.")
    if "Significant Deficiency" in present:
        return ("SIGNIFICANT DEFICIENCY",
                "Significant deficiencies exist and require audit-committee attention. "
                "Remediation is needed before relying on affected automated controls.")
    if "Control Deficiency" in present:
        return ("CONTROL DEFICIENCY",
                "Control deficiencies exist but are not individually material. "
                "Remediate and re-test.")
    return ("EFFECTIVE", "No deficiencies identified. ITGC environment operating effectively.")


def status_chart(df):
    counts = (df.groupby(["ITGC_Domain", "Test_Result"]).size()
              .unstack(fill_value=0).reindex(index=DOMAINS, columns=RESULTS, fill_value=0))
    fig, ax = plt.subplots(figsize=(9, 5))
    bottom = [0] * len(counts)
    for res in RESULTS:
        ax.barh(counts.index, counts[res], left=bottom,
                color=RESULT_COLORS[res], label=res)
        bottom = [b + v for b, v in zip(bottom, counts[res])]
    ax.set_xlabel("Number of controls", fontweight="bold")
    ax.set_title("NorthStar Lending — SOX ITGC Test Results by Domain", fontweight="bold")
    ax.legend(title="Test result", loc="lower right")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUT / "itgc-status-by-domain.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_summary(df, label, narrative):
    total = len(df)
    passed = (df["Test_Result"] == "Pass").sum()
    rate = passed / total * 100
    by_res = df["Test_Result"].value_counts().reindex(RESULTS, fill_value=0)
    by_sev = df["Deficiency_Severity"].value_counts().reindex(SEVERITY_ORDER, fill_value=0)
    lines = ["# SOX ITGC Assessment Summary (auto-generated)\n",
             f"**Overall conclusion:** {label}\n", f"{narrative}\n",
             f"- Controls tested: **{total}**",
             f"- Operating effectively (Pass): **{passed}** ({rate:.0f}%)",
             f"- Exceptions: **{int(by_res['Exception'])}**  |  Failures: **{int(by_res['Fail'])}**\n",
             "## Deficiencies by severity\n", "| Severity | Count |", "|----------|-------|"]
    lines += [f"| {s} | {int(by_sev[s])} |" for s in SEVERITY_ORDER]
    lines += ["\n## Open deficiencies\n", "| Control | Domain | Result | Severity |",
              "|---------|--------|--------|----------|"]
    for _, r in df[df["Test_Result"] != "Pass"].iterrows():
        lines.append(f"| {r.Control_ID} | {r.ITGC_Domain} | {r.Test_Result} | {r.Deficiency_Severity} |")
    (OUT / "itgc-assessment-summary.md").write_text("\n".join(lines) + "\n")


def main():
    df = load()
    label, narrative = overall_conclusion(df)
    write_summary(df, label, narrative)
    status_chart(df)
    total = len(df); passed = (df["Test_Result"] == "Pass").sum()
    print(f"ITGC controls tested: {total}  |  effective: {passed} ({passed/total*100:.0f}%)")
    print(f"Overall conclusion: {label}\n")
    print("Open deficiencies:")
    for _, r in df[df["Test_Result"] != "Pass"].iterrows():
        print(f"  {r.Control_ID}  [{r.Deficiency_Severity:22}] {r.Control_Objective}")
    print(f"\nOutputs written to {OUT}/")


if __name__ == "__main__":
    main()
