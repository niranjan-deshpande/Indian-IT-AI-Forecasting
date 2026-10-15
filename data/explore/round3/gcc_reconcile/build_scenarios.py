"""GCC vs Nasscom reconciliation scenarios (thousands of persons). Inputs: reconcile_inputs.csv (sources)."""
import csv, os
here = os.path.dirname(os.path.abspath(__file__))
SR24 = "https://nasscom.in/sites/default/files/media_pdf/nasscom-strategic-review-2024-press-release.pdf"
SR25 = "https://nasscom.in/sites/default/files/media_pdf/Nasscom%20SR%20Press%20release.pdf"
SR26 = "https://nasscom.in/modules/custom/nasscom_general/docs/Nasscom-Strategic%20Review-2026-Executive%20Summary.pdf"
Z24 = "https://nasscom.in/knowledge-center/publications/india-gcc-landscape-report-5-year-journey"
Z23 = "https://nasscom.in/knowledge-center/publications/gcc-40-india-redefining-globalization-blueprint"
Z26 = "https://zinnov.com/centers-of-excellence/zinnov-nasscom-india-gcc-landscape-2026-report/"
IANS = "https://ianslive.in/gccs-projected-to-create-up-to-28-lakh-jobs-in-india-by-2030--20240912133249"
HIRE = "https://www.business-standard.com/industry/news/gcc-hiring-for-fy26-to-remain-strong-may-again-outpace-it-services-125030600994_1.html ; https://www.india-briefing.com/news/indias-workforce-trends-shift-toward-gccs-over-it-firms-36459.html/"
TOP6 = "data/explore/round3/gcc/top6_headcount_fy.csv"

# Nasscom industry net additions, within-vintage (k)
nas = {"FY23-26": (60 + 126 + 135, 60 + 133 + 135), "FY24-26": (126 + 135, 133 + 135)}
top6 = {"FY23-26": (1618023 - 1679489) / 1000, "FY24-26": (1618023 - 1605986) / 1000}
# GCC change scenarios (all functions), (low, central, high) in k
g24_26_proj = (1900 * (2500 / 1900) ** (2 / 6) - 1900, 1900 * (2800 / 1900) ** (2 / 6) - 1900)
gcc = {
 "FY23-26": [
  ("S1 editions chained across restatement (invalid)", (700, 700, 700), "1.66m FY23 (old basis) -> 2.36m FY26", f"{Z23} ; {Z26}"),
  ("S2 Zinnov restated basis, FY23 back-cast", (1900 - (1900 - 60) + 460, 540, 1900 - 1900 / 1.063 + 460),
   "FY24 1.90m; FY23 = 1.90m - 60k (FY24 net hiring) or 1.90/1.063 (6.3%/yr from '+36% FY19-24', secondary); FY26 2.36m", f"{Z24} ; {Z26}"),
  ("S3 staffing-firm net hiring sum", (370, 385, 400), "FY24 ~60k + FY25 110-140k + FY26 ~200k", HIRE),
  ("S4 2024-edition trajectory (no coverage expansion)", (60 + g24_26_proj[0], 60 + sum(g24_26_proj) / 2, 60 + g24_26_proj[1]),
   "FY23-24 +60k; FY24-26 at pace to reach 2.5-2.8m by FY30 (4.7-6.7%/yr)", f"{IANS} ; {HIRE}"),
 ],
 "FY24-26": [
  ("S2 Zinnov FY24 1.90m -> FY26 2.36m", (460, 460, 460), "as published", f"{Z24} ; {Z26}"),
  ("S3 staffing-firm net hiring sum", (310, 325, 340), "FY25 110-140k + FY26 ~200k", HIRE),
  ("S4 2024-edition trajectory", (g24_26_proj[0], sum(g24_26_proj) / 2, g24_26_proj[1]), "4.7-6.7%/yr", IANS),
 ],
}
shares = (0.55, 0.67, 0.80)  # tech (IT + ER&D) share of GCC staff; Mega GCC ~0.67, BFSI ~0.47, ER&D alone 0.42
rows = []
for win, scen in gcc.items():
    n_lo, n_hi = nas[win]; n_c = (n_lo + n_hi) / 2; t = top6[win]
    for name, (lo, c, hi), basis, url in scen:
        rest_c = n_c - c - t
        rest_lo = n_lo - max(lo, hi) - t; rest_hi = n_hi - min(lo, hi) - t
        rows.append({
            "window": win, "scenario": name, "gcc_change_all_functions_k_low": round(min(lo, hi)),
            "gcc_change_all_functions_k_central": round(c), "gcc_change_all_functions_k_high": round(max(lo, hi)),
            "gcc_tech_change_k_share0.55": round(c * shares[0]), "gcc_tech_change_k_share0.67": round(c * shares[1]),
            "gcc_tech_change_k_share0.80": round(c * shares[2]),
            "nasscom_total_change_k": f"{n_lo}-{n_hi}", "top6_change_k_global": round(t, 1),
            "rest_of_industry_change_k_central": round(rest_c), "rest_range_k": f"{round(rest_lo)} to {round(rest_hi)}",
            "assumes": "Nasscom total includes GCCs (all functions); rest = Nasscom - GCC - top6",
            "gcc_basis": basis, "source_url": f"{url} ; Nasscom: {SR24} ; {SR25} ; {SR26} ; top6: {TOP6}"})
    rows.append({"window": win, "scenario": "S0 IF Nasscom total EXCLUDED GCCs (rejected by SR2025 note)",
                 "nasscom_total_change_k": f"{n_lo}-{n_hi}", "top6_change_k_global": round(t, 1),
                 "rest_of_industry_change_k_central": round(n_c - t), "rest_range_k": f"{round(n_lo - t)} to {round(n_hi - t)}",
                 "assumes": "rest = Nasscom - top6; GCC additive", "gcc_basis": "n/a", "source_url": f"{SR24} ; {SR25} ; {SR26} ; {TOP6}"})
out = os.path.join(here, "gcc_scenarios.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["window"], "|", r["scenario"][:48].ljust(48), "| GCC", r.get("gcc_change_all_functions_k_low"), r.get("gcc_change_all_functions_k_central"), r.get("gcc_change_all_functions_k_high"),
          "| tech", r.get("gcc_tech_change_k_share0.55"), r.get("gcc_tech_change_k_share0.67"), r.get("gcc_tech_change_k_share0.80"),
          "| N", r["nasscom_total_change_k"], "| T6", r["top6_change_k_global"], "| rest", r["rest_of_industry_change_k_central"], "(", r["rest_range_k"], ")")
