# -*- coding: utf-8 -*-
"""Testing advanced functionality of the base class."""
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["fkiraly"]

import pytest

from sktime.datatypes import check_is_mtype, convert
from sktime.forecasting.arima import ARIMA
from sktime.utils._testing.panel import _make_panel_X

PANEL_MTYPES = ["pd-multiindex", "nested_univ", "numpy3D"]


@pytest.mark.parametrize("mtype", PANEL_MTYPES)
def test_vectorization_series_to_panel(mtype):
    """Test that forecaster vectorization works for Panel data.

    This test passes Panel data to the ARIMA forecaster which internally has an
    implementation for Series only, so the BaseForecaster has to vectorize.
    """
    n_instances = 10

    y = _make_panel_X(n_instances=n_instances)
    y = convert(y, from_type="nested_univ", to_type=mtype)

    y_pred = ARIMA().fit(y).predict([1, 2, 3])
    valid, _, metadata = check_is_mtype(y_pred, mtype, return_metadata=True)

    msg = (
        f"vectorization of forecasters does not work for test example "
        f"of mtype {mtype}, using the ARIMA forecaster"
    )

    assert valid, msg

    y_pred_instances = metadata["n_instances"]
    msg = (
        f"vectorization test produces wrong number of instances "
        f"expected {n_instances}, found {y_pred_instances}"
    )

    assert y_pred_instances == n_instances, msg

    y_pred_equal_length = metadata["is_equal_length"]
    msg = (
        "vectorization test produces non-equal length Panel forecast, should be "
        "equal length, and length equal to the forecasting horizon [1, 2, 3]"
    )
    assert y_pred_equal_length, msg