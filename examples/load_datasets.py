"""
Reference loader for the four RT-FDD CSV datasets.

All timestamps in the published CSVs are Unix epoch milliseconds (UTC).
This module reads them as integers and provides a helper to convert to
pandas datetime when needed.

Usage:
    from load_datasets import load_all
    pnp_od, pnp_asd, furnace_od, furnace_asd = load_all()
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

PICKNPLACE_OD  = DATA_DIR / "picknplace_od.csv"
PICKNPLACE_ASD = DATA_DIR / "picknplace_asd.csv"
FURNACE_OD     = DATA_DIR / "furnace_od.csv"
FURNACE_ASD    = DATA_DIR / "furnace_asd.csv"


def _merge_pnp_normal_classes(df: pd.DataFrame) -> pd.DataFrame:
    """Merge PnP normal-axis variants (classes 1, 2) into class 0.

    fault_class = 10*sim + axis produces classes 0, 1, 2 for sim=0 (Normal)
    on axes X, Y, Z. All represent normal operation and are merged into a
    single class 0 to match the 7-class scheme used throughout the article.
    """
    df.loc[df["fault_class"].isin([1, 2]), "fault_class"] = 0
    return df


def load_picknplace_od() -> pd.DataFrame:
    """Pick-and-Place Original Dataset (real machine logs)."""
    df = pd.read_csv(PICKNPLACE_OD, index_col=0)
    df = df.dropna(subset=["sim", "axis", "cycle"])
    df["fault_class"] = (10 * df["sim"] + df["axis"]).astype(int)
    return _merge_pnp_normal_classes(df)


_VALID_PNP_FAULT_CLASSES = [0, 10, 11, 12, 20, 21, 22, 30, 31, 32]


def load_picknplace_asd(drop_artifact_classes: bool = True) -> pd.DataFrame:
    """Pick-and-Place Aleatory Simulated Dataset (digital twin).

    A small number of rows in the raw ASD have corrupted sim/axis values
    that produce fault_class values outside the documented 10-class
    scheme (e.g. 107, 108, 109). Set drop_artifact_classes=False to
    inspect them; the default matches the article's analysis pipeline.
    """
    df = pd.read_csv(PICKNPLACE_ASD)
    df = df.drop(columns=["Numero"], errors="ignore")
    df = df.dropna(subset=["sim", "axis", "cycle"])
    df["fault_class"] = (10 * df["sim"] + df["axis"]).astype(int)
    df = _merge_pnp_normal_classes(df)
    if drop_artifact_classes:
        df = df[df["fault_class"].isin(_VALID_PNP_FAULT_CLASSES)]
    return df


def load_furnace_od() -> pd.DataFrame:
    """Furnace Original Dataset (real machine logs)."""
    return pd.read_csv(FURNACE_OD, index_col=0)


def load_furnace_asd() -> pd.DataFrame:
    """Furnace Aleatory Simulated Dataset (digital twin)."""
    return pd.read_csv(FURNACE_ASD)


def load_all():
    """Load all four datasets. Returns (pnp_od, pnp_asd, furnace_od, furnace_asd)."""
    return (
        load_picknplace_od(),
        load_picknplace_asd(),
        load_furnace_od(),
        load_furnace_asd(),
    )


def to_datetime(series: pd.Series) -> pd.Series:
    """Convert an epoch-ms timestamp column to a pandas datetime (UTC)."""
    return pd.to_datetime(series, unit="ms", utc=True)


if __name__ == "__main__":
    pnp_od, pnp_asd, furn_od, furn_asd = load_all()
    print(f"Pick-and-Place OD:  {len(pnp_od):>7,} rows, {pnp_od['fault_class'].nunique()} classes")
    print(f"Pick-and-Place ASD: {len(pnp_asd):>7,} rows, {pnp_asd['fault_class'].nunique()} classes")
    print(f"Furnace OD:         {len(furn_od):>7,} rows, {furn_od['class'].nunique()} classes")
    print(f"Furnace ASD:        {len(furn_asd):>7,} rows, {furn_asd['class'].nunique()} classes")
    print()
    print(f"Example PnP OD timestamp (epoch ms): {pnp_od['timestamp'].iloc[0]}")
    print(f"Same as UTC datetime: {to_datetime(pnp_od['timestamp']).iloc[0]}")
