# RT-FDD Datasets — Pick-and-Place and Electric Furnace

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20576461.svg)](https://doi.org/10.5281/zenodo.20576461)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

Four benchmark datasets for Real-Time Fault Detection and Diagnosis (RT-FDD)
research on discrete manufacturing machines. Each machine (Pick-and-Place
and Electric Furnace) is provided in two versions:

- **OD** — Original Dataset: deterministic fault conditions logged from a
  closed-loop real-time simulation running on a SoftPLC stack
  (Modbus TCP + OPC UA).
- **ASD** — Aleatory Simulated Dataset: the same scenarios with bounded
  random variability injected into parameters, sensor noise, and timing,
  to emulate realistic industrial uncertainty.

The datasets are organised per operating cycle and preserve event timing,
execution order, and continuous sensor behaviour. They support both
end-of-cycle and intra-cycle RT-FDD evaluation.

> If you use these datasets, please cite the article and this release
> (see [CITATION.cff](CITATION.cff) and the Zenodo DOI in the badge below).

## Files

```
data/
  picknplace_od.csv     20 MB,   206,169 rows,  7 classes
  picknplace_asd.csv     9 MB,   148,556 rows, 10 classes (after artifact filter)
  furnace_od.csv        25 MB,   337,854 rows,  4 classes
  furnace_asd.csv       44 MB,   440,659 rows,  6 classes
examples/
  load_datasets.py      Reference loader for all 4 CSVs
  plot_cycle.py         Minimal example: plot one cycle per dataset
  requirements.txt      pandas, numpy, matplotlib
```

## Timestamps

**All four CSVs use Unix epoch milliseconds (UTC)** in the `timestamp`
column. Convert to a pandas datetime with:

```python
import pandas as pd
ts = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
```

## Column reference

### Pick-and-Place (PnP)

| Column        | Type   | Meaning                                                  |
|---------------|--------|----------------------------------------------------------|
| `timestamp`   | int64  | Sample time (Unix epoch ms, UTC)                         |
| `x_sp`,`y_sp`,`z_sp`             | float | Position setpoints per axis              |
| `x_pos_AI`,`y_pos_AI`,`z_pos_AI` | float | Measured analog position per axis        |
| `x_fwd`,`x_bwd`,`y_fwd`,`y_bwd`,`z_up`,`z_down` | bool | Discrete movement signals     |
| `cycle`       | int    | Cycle index within the run                               |
| `axis`        | int    | 0 = X, 1 = Y, 2 = Z (axis under fault, if any)           |
| `sim`         | int    | Fault family: 0 = Normal, 1 = Obstruction, 2 = Speed Loss, 3 = combined (ASD only) |
| `intensity`   | float  | Fault intensity parameter (ASD only)                     |

Derived `fault_class = 10*sim + axis` after merging Normal axis variants:

| fault_class | Description           |
|-------------|-----------------------|
| 0           | Normal                |
| 10, 11, 12  | F1–F3 Obstruction X/Y/Z |
| 20, 21, 22  | F4–F6 Speed Loss X/Y/Z |
| 30, 31, 32  | F7–F9 Combined (ASD)  |

### Electric Furnace

| Column        | Type   | Meaning                                                  |
|---------------|--------|----------------------------------------------------------|
| `timestamp`   | int64  | Sample time (Unix epoch ms, UTC)                         |
| `temperature` | float  | Measured temperature (°C)                                |
| `door_open`,`door_closed`,`heat_on`,`max_power` | bool | Discrete state signals          |
| `cycle_count` | int    | Cycle index (cycles also delimited by door_closed rising edges) |
| `class`       | str    | Fault class name (e.g. `Normal`, `0.98xTemp`, `2_degree_offset`, `5_degree_dev`) |
| `error_temp`,`error_power`,`pure_temp` | float | ASD-only diagnostic columns       |

## Quickstart

```bash
pip install -r examples/requirements.txt
python examples/load_datasets.py   # prints row counts + class counts
python examples/plot_cycle.py      # saves cycle_examples.png
```

## Article

These datasets accompany the article:

> Fonseca, H.; Cintra, P.; Silva, R.; Andrade, E.; Rativa, D.;
> Maciel, A.M.A.; Leite, D. *Benchmark Datasets for Real-Time Fault
> Detection and Diagnosis on Discrete Manufacturing Machines*. Sensors
> (in submission).

See the article for the closed-loop simulation architecture, the fault
injection methodology, and four reuse studies (AutoML supervised
classification, unsupervised anomaly detection, robustness analysis,
Digital Twin–enhanced early detection).

## Reproducibility

This repository is archived on Zenodo on every Git release, which
produces a citable DOI. **For paper references, cite the v1.0.0 DOI**
(shown in the Zenodo badge above) — the `main` branch may evolve, but
released versions are immutable.

## Citing

A `CITATION.cff` file is provided. GitHub renders a "Cite this repository"
button in the sidebar that produces BibTeX/APA from it. Please cite both
the article and the dataset DOI.

## License

[CC BY 4.0](LICENSE) — free to use and adapt with attribution.

---

### Zenodo integration (one-time setup, for maintainers)

To mint a DOI for a release:

1. Sign in at <https://zenodo.org/> with your GitHub account.
2. Visit <https://zenodo.org/account/settings/github/> and flip the
   switch ON for this repository.
3. Push the `v1.0.0` Git tag (or create a GitHub Release). Zenodo
   archives the tagged commit automatically and assigns a DOI.
4. Update the DOI badge at the top of this README and the
   `related_identifiers` block in `.zenodo.json`.
