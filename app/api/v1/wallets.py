import uuid

from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.wallet import Wallet
from app.schemas.wallet import OperationType, WalletOperationIn, WalletOut


# Роутер для API-эндпоинтов работы с кошельками (получение баланса и операции)
router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


@router.get("/{wallet_uuid}", response_model=WalletOut)
async def get_wallet_balance(
    wallet_uuid: uuid.UUID,
    session: AsyncSession = Depends(get_session)
) -> WalletOut:
    result = await session.execute(select(Wallet).where(Wallet.id == wallet_uuid))
    wallet = result.scalar_one_or_none()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletOut(wallet_uuid=str(wallet.id), balance=wallet.balance)


@router.post("/{wallet_uuid}/operation", response_model=WalletOut)
async def wallet_operation(
    wallet_uuid: uuid.UUID,
    payload: WalletOperationIn,
    session: AsyncSession = Depends(get_session),
) -> WalletOut:

    # Проверяем, существует ли кошелек
    exists = await session.execute(select(Wallet.id).where(Wallet.id == wallet_uuid))
    if exists.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # DEPOSIT: атомарный update
    if payload.operation_type == OperationType.DEPOSIT:
        stmt = (
            update(Wallet)
            .where(Wallet.id == wallet_uuid)
            .values(balance=Wallet.balance + payload.amount)
            .returning(Wallet.id, Wallet.balance)
        )
        row = (await session.execute(stmt)).one()
        await session.commit()
        return WalletOut(wallet_uuid=str(row.id), balance=row.balance)

    # WITHDRAW: атомарно и без ухода в минус
    stmt = (
        update(Wallet)
        .where(Wallet.id == wallet_uuid, Wallet.balance >= payload.amount)
        .values(balance=Wallet.balance - payload.amount)
        .returning(Wallet.id, Wallet.balance)
    )
    row = (await session.execute(stmt)).one_or_none()

    if row is None:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient funds"
        )
    await session.commit()
    return WalletOut(wallet_uuid=str(row.id), balance=row.balance)
