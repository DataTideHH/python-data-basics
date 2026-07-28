# Project Status

## Status

**Portfolio-complete / maintenance mode**

The core scope of `python-data-basics` is complete as of July 2026. The repository now provides a small but coherent Python Data/BI workflow from imperfect CSV input through validation, auditable rejection, KPI reconciliation, reporting and notebook verification.

The repository remains active and public, but it is no longer intended to grow through unrelated examples or speculative platform features.

## Completed scope

The completed portfolio scope includes:

- reproducible Python 3.12 project setup
- explicit runtime, notebook, ML and development dependency groups
- deterministic pandas baseline check
- synthetic CSV fixture with documented quality defects
- required-column, type, missing-value, range and duplicate controls
- cleaned and rejected row exports
- row-level rejection reasons and source-row lineage
- module KPI aggregation
- independent KPI recalculation and reconciliation
- deterministic reporting summaries and SVG charts
- clean environment and reporting notebooks
- pytest, Ruff and bytecode checks
- end-to-end GitHub Actions on Ubuntu and Windows
- explicit data-safety and scope boundaries

## Maintenance policy

Further changes should normally be limited to:

- compatibility updates for supported dependencies or GitHub Actions
- defect corrections
- clearer documentation
- security or credential-safety improvements
- small test additions required to protect existing behaviour

Changes should preserve the existing control totals unless the fixture or business rules are deliberately revised and documented.

## Out of scope

The following additions are intentionally not planned for this repository:

- larger artificial datasets added only to create scale
- machine learning claims based on the small synthetic fixture
- Streamlit or another dashboard layer
- Power BI files unrelated to the repository's current purpose
- cloud deployment or orchestration
- streaming or distributed processing
- database infrastructure already demonstrated in other DataTideHH repositories
- unrelated Python language exercises

Those subjects belong in dedicated projects when there is a clear business question and sufficient evidence.

## Portfolio role

This repository serves as the tested Python foundation within the wider DataTideHH portfolio. It demonstrates that a bounded Data/BI workflow can be:

1. understood from its input contract
2. executed locally
3. tested automatically
4. reconciled before reporting
5. reviewed through code, outputs, charts and documentation
6. explained without overstating its scale or maturity

Related projects provide deeper evidence for SQL Server, APIs, public data, Power BI preparation and infrastructure-oriented data workflows.
