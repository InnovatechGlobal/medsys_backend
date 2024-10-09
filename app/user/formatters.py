from app.user import models


async def format_user(user: models.User):
    """
    Format user obj to dict
    """
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "gender": user.gender,
        "medical_id": user.medical_id,
        "dob": user.dob,
        "country": user.country,
        "account_type": user.account_type,
        "is_active": user.is_active,
    }
