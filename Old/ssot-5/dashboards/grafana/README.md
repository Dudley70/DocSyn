# SSOT Dashboards (Grafana)

Generated: 2025-09-08 12:02 UTC

These are **starter dashboards** that visualise the KPIs defined in the SSOT blueprints.

## How to import
1. In Grafana, go to **Dashboards → Import**.
2. Upload one of the JSON files in this folder (start with `ssot_overview.json`).
3. Select your **Prometheus** and **Loki** datasources for variables `DS_PROM` and `DS_LOKI` when prompted.
4. Set the `env` and `service` variables as appropriate (default is `prod`).

## Metric expectations
The expressions use placeholder metric names like `agent_tasks_executed_total`. Map these to your actual metrics via recording or relabeling rules if needed.

## Files
- `ssot_overview.json` — cross-blueprint KPIs.
- `blueprint_BP-*.json` — KPIs for each blueprint (Documenter, Guardian, Janitor, Tester, CI/CD, Adaptive, Orchestrator).

