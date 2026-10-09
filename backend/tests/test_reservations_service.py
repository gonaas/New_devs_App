from decimal import Decimal

import pytest

from app.core import database_pool
from app.core.database_pool import DatabasePool
from app.services import reservations


@pytest.mark.asyncio
async def test_database_failure_surfaces_instead_of_returning_mock_data(monkeypatch):
    unreachable = DatabasePool()
    monkeypatch.setattr(database_pool.settings, "database_url", "postgresql://x:x@127.0.0.1:1/none")
    monkeypatch.setattr(reservations, "db_pool", unreachable, raising=False)

    with pytest.raises(Exception):
        await reservations.calculate_total_revenue("prop-001", "tenant-a")


@pytest.mark.asyncio
async def test_month_bounds_use_property_timezone():
    # res-tz-1 checks in 2024-02-29 23:30 UTC = 2024-03-01 00:30 in Europe/Paris.
    march = await reservations.calculate_monthly_revenue("prop-001", "tenant-a", 3, 2024)
    february = await reservations.calculate_monthly_revenue("prop-001", "tenant-a", 2, 2024)

    assert march == Decimal("2250.00")
    assert february == Decimal("0.00")
