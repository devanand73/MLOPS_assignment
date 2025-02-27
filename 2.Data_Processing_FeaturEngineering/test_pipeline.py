# File: tests/test_pipeline.py
import pytest
import pandas as pd
import numpy as np
from feature_pipeline import FeaturePipeline

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'num_feat': [1, 2, np.nan, 4],
        'cat_feat': ['A', 'B', 'A', None],
        'target': [0, 1, 0, 1]
    })

def test_missing_value_imputation(sample_data):
    config = {
        'numerical_features': ['num_feat'],
        'categorical_features': ['cat_feat'],
        'target': 'target',
        'version': '0.1'
    }

    pipeline = FeaturePipeline(config)
    transformed = pipeline.run(sample_data)

    # Check no missing values
    assert not np.isnan(transformed).any()

def test_feature_selection():
    # Test feature importance scoring
    pass