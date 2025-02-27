# monitor_drift.py
import dvc.api
from scipy.stats import ks_2samp

def detect_drift(current_data, previous_version='HEAD~1'):
    # Get previous version
    prev_path = dvc.api.get_url("data/processed", rev=previous_version)

    # Load datasets
    current = pd.read_parquet(current_data)
    previous = pd.read_parquet(prev_path)

    # Compare distributions
    drift_detected = {}
    for col in current.columns:
        statistic, pvalue = ks_2samp(current[col], previous[col])
        if pvalue < 0.05:
            drift_detected[col] = pvalue

    return drift_detected