from sqlalchemy.ext.asyncio import AsyncSession

from app.common.crud import CRUDBase
from app.hospital import models


class HospitalCRUD(CRUDBase[models.Hospital]):
    """
    CRUD Class for hospitals
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.Hospital, db=db)


class HospitalStaffCRUD(CRUDBase[models.HospitalStaff]):
    """
    CRUD Class for hospital staff
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.HospitalStaff, db=db)
