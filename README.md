# Prods

Frontend automation tests for the deployed restaurant website live in this repo as a `pytest` + Selenium suite.

## Restaurant Frontend Test Suite

The restaurant UI tests are organized under the `tests/` folder:

- `tests/test_restaurant_menu.py` covers page load, search, and category filtering.
- `tests/test_restaurant_order_modal.py` covers create-order modal behavior, validation alerts, quantity changes, and total updates.
- `tests/test_restaurant_check_order.py` covers check-order modal behavior and input validation.
- `tests/conftest.py` contains the shared Selenium driver fixture and modal helpers.

Legacy learning files are still present for reference, but they are no longer the active suite:

- `test_TestingRestaurantWebsite.py` now skips at module level.
- `test_belejarselenium.py` only runs when executed directly, so VS Code test discovery will not open Chrome by itself.

## Run The Tests

Install dependencies in your virtual environment first, then run:

```powershell
pytest -q
```

To collect tests without running them:

```powershell
pytest --collect-only -q
```

## Useful Environment Variables

- `RESTAURANT_BASE_URL` overrides the deployed site URL.
- `RESTAURANT_UI_TIMEOUT` changes the Selenium wait timeout in seconds.
- `SELENIUM_HEADLESS=0` opens Chrome visibly for debugging. By default the suite runs headless.

## Notes

- The current suite is intentionally scoped to frontend behavior only.
- Success paths that require a live backend order API are not part of this frontend-only suite yet.
- VS Code test discovery is configured through `pytest.ini` to use the `tests/` folder.
