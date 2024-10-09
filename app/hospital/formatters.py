from app.hospital import models


async def format_hospital(hosp: models.Hospital):
    """
    Format hospital obj to dict
    """
    return {
        "id": hosp.id,
        "name": hosp.name,
        "address": hosp.address,
        "email": hosp.email,
        "phone": hosp.phone,
    }
