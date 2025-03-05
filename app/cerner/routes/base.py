import calendar
import random

from fastapi import APIRouter

from app.cerner.schemas import response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()


@router.get(
    "/home",
    summary="Get cerner homepage",
    response_description="The details of the cerner homepage",
    status_code=200,
    response_model=response.CernerHomepageResponse,
)
async def route_cerner_home(_: CurrentUser):
    """
    This endpoint returns the details of the oracle cerner homepage
    """

    return {
        "data": {
            "tno_patients": random.randint(10, 1000),
            "tno_admissions": random.randint(10, 1000),
            "tno_cases": random.randint(10, 1000),
            "discharge_rate": round(100 / random.randint(1, 100), 1),
            "patient_stats": {
                "weekly": [
                    {
                        "label": i,
                        "tn_admitted": random.randint(1, 10),
                        "tn_discharged": random.randint(1, 10),
                    }
                    for i in [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ]
                ],
                "monthly": [
                    {
                        "label": str(i),
                        "tn_admitted": random.randint(1, 10),
                        "tn_discharged": random.randint(1, 10),
                    }
                    for i in range(1, 29)
                ],
                "yearly": [
                    {
                        "label": i,
                        "tn_admitted": random.randint(10, 300),
                        "tn_discharged": random.randint(10, 300),
                    }
                    for i in list(calendar.month_name)[1:]
                ],
            },
            "patient_dist": [
                {"dept": i, "value": random.randint(300, 500)}
                for i in ["Nephrology", "Pediatrics", "Surgery", "Psychiatry"]
            ],
            "clinic_metrics": [
                {
                    "section": "Vital Signs Overview",
                    "metric": [
                        {
                            "name": "High BP Cases",
                            "obs": "10 patients with BP >140/90 mmHg.",
                        }
                    ],
                },
                {
                    "section": "Lab Results Summary",
                    "metric": [
                        {
                            "name": "Elevated Glucose Levels",
                            "obs": "3 patients with glucose >200 mg/dL",
                        }
                    ],
                },
            ],
        }
    }
