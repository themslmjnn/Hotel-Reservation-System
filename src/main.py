from fastapi import FastAPI

import src.models
from src.auth import router
from src.users import router_admin, router_public, router_staff

app = FastAPI(title="Hotel Reservation API")


app.include_router(router.router)
app.include_router(router_admin.router)
app.include_router(router_staff.router)
app.include_router(router_public.router)