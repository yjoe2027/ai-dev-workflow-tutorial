"""Smoke test: run app.py for real with Streamlit's AppTest."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parent.parent / "app.py"


@pytest.fixture(scope="module")
def app():
    return AppTest.from_file(str(APP_PATH)).run(timeout=30)


def test_app_runs_without_errors(app):
    assert not app.exception
    assert not app.error


def test_app_shows_title(app):
    assert app.title[0].value == "ShopSmart Sales Dashboard"


def test_app_shows_kpis_from_prd_expected_output(app):
    kpis = {metric.label: metric.value for metric in app.metric}
    assert kpis == {"Total Sales": "$116,500", "Total Orders": "482"}


def test_app_shows_charts(app):
    assert len(app.get("plotly_chart")) >= 1
