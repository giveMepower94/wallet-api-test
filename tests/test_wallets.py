import asyncio
import pytest

pytestmark = pytest.mark.asyncio


async def test_get_wallet_balance_ok(client, wallet_id):
    resp = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["wallet_uuid"] == str(wallet_id)
    assert data["balance"] == 0


async def test_get_wallet_balance_404(client):
    resp = await client.get("/api/v1/wallets/11111111-1111-1111-1111-111111111111")
    assert resp.status_code == 404


async def test_deposit_increases_balance(client, wallet_id):
    resp = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )
    assert resp.status_code == 200
    assert resp.json()["balance"] == 1000


async def test_withdraw_decreases_balance(client, wallet_id):
    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )

    resp = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 400}
    )

    assert resp.status_code == 200
    assert resp.json()["balance"] == 600


async def test_withdraw_insufficient_funds_returns_409(client, wallet_id):
    resp = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 10000}
    )
    assert resp.status_code == 409


async def test_concurrent_withdraw_is_atomic(client, wallet_id):
    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )

    async def withdraw_700():
        return await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "WITHDRAW", "amount": 700},
        )
    res1, res2 = await asyncio.gather(withdraw_700(), withdraw_700())
    statuses = sorted([res1.status_code, res2.status_code])
    assert statuses == [200, 409]

    # Итоговый баланс должен быть 300
    final_res = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert final_res.status_code == 200
    assert final_res.json()["balance"] == 300
