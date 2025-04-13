from sqlalchemy.ext.asyncio import AsyncSession

from app.medchat.crud import MedChatCRUD
from app.medchat.exceptions import MedChatNotFound


async def get_medchat_by_id(id: int, db: AsyncSession, raise_exc: bool = True):
    """
    Get medchat by ID

    Args:
        id (int): The ID of the medchat
        db (AsyncSession): The database
        raise_exc (bool, optional): raise a 404 if not found. Defaults to True.

    Raises:
        MedChatNotFound

    Returns:
        models.MedChat: The medchat obj
    """
    # Init crud
    medchat_crud = MedChatCRUD(db=db)

    # Get obj
    obj = await medchat_crud.get(id=id)

    if not obj and raise_exc:
        raise MedChatNotFound()

    return obj


async def get_medchat_by_patient_id(id: str, db: AsyncSession, raise_exc: bool = True):
    """
    Get medchat by patient ID

    Args:
        id (int): The ID of the patient
        db (AsyncSession): The database
        raise_exc (bool, optional): raise a 404 if not found. Defaults to True.

    Raises:
        MedChatNotFound

    Returns:
        models.MedChat: The medchat obj
    """
    # Init crud
    medchat_crud = MedChatCRUD(db=db)

    # Get obj
    obj = await medchat_crud.get(patient_id=id)

    if not obj and raise_exc:
        raise MedChatNotFound()

    return obj
