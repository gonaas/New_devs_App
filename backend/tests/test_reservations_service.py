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
