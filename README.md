# Prods

Frontend automation tests for the deployed restaurant website live in this repo as a `pytest` + Selenium suite with `pytest-bdd` feature files and optional `pytest-html` reporting.

## Restaurant Frontend Test Suite

The restaurant UI tests are organized under the `tests/` folder:

- `tests/features/restaurant_menu.feature` covers page load, search, category filtering, Today's Recommendation, People Favorites, and Chef's Pick.
- `tests/features/restaurant_order_modal.feature` covers create-order modal behavior, validation alerts, quantity changes, and total updates.
- `tests/features/restaurant_check_order.feature` covers check-order modal behavior and input validation.
- `tests/test_restaurant_menu.py`, `tests/test_restaurant_order_modal.py`, and `tests/test_restaurant_check_order.py` map the feature files into pytest scenarios.
- `tests/conftest.py` contains the shared Selenium driver fixture, `pytest-bdd` step definitions, and a custom `pytest-html` report title.

Legacy Selenium learning work is still present for reference, but it is no longer the active suite:

- `test_TestingRestaurantWebsite.py` now skips at module level.
- `test_belejarselenium2.py` contains older practice tests against the Selenium demo web form.

## Run The Tests

Install dependencies in your virtual environment first, then run:

```powershell
pytest -q
```

To collect tests without running them:

```powershell
pytest --collect-only -q
```

To generate an HTML report:

```powershell
pytest -q --html=reports/e-restaurant-report.html --self-contained-html
```

## Useful Environment Variables

- `RESTAURANT_BASE_URL` overrides the deployed site URL.
- `RESTAURANT_UI_TIMEOUT` changes the Selenium wait timeout in seconds.
- `SELENIUM_HEADLESS=0` opens Chrome visibly for debugging. By default the suite runs headless.

## Notes

- The current suite is intentionally scoped to frontend behavior only.
- Success paths that require a live backend order API are not part of this frontend-only suite yet.
- VS Code test discovery is configured through `pytest.ini` to use the `tests/` folder.
- `pytest-bdd` uses `tests/features` as the base directory for Gherkin feature files.
