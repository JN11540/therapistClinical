from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from core.config import TEMPLATE_DIR

router = APIRouter(tags=["pages"])

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/")
async def page_login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.get("/register")
async def page_register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@router.get("/home")
async def page_home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@router.get("/edit-clinician-profile")
async def page_edit_clinician_profile(request: Request):
    return templates.TemplateResponse(request, "edit_clinician_profile.html")


@router.get("/add-patient")
async def page_add_patient(request: Request):
    return templates.TemplateResponse(request, "add_patient.html")


@router.get("/edit-patient")
async def page_edit_patient(request: Request):
    return templates.TemplateResponse(request, "edit_patient.html")


@router.get("/patient-detail")
async def page_patient_detail(request: Request):
    return templates.TemplateResponse(request, "patient_detail.html")


@router.get("/add-assessment")
async def page_add_assessment(request: Request):
    return templates.TemplateResponse(request, "add_assessment.html")


@router.get("/edit-assessment")
async def page_edit_assessment(request: Request):
    return templates.TemplateResponse(request, "edit_assessment.html")


@router.get("/treatment-plan")
async def page_treatment_plan(request: Request):
    return templates.TemplateResponse(request, "treatment_plan.html")


@router.get("/patient-treatment-plan")
async def page_patient_treatment_plan(request: Request):
    return templates.TemplateResponse(request, "patient-treatment-plan.html")


@router.get("/edit_patient-treatment-plan")
async def page_edit_patient_treatment_plan(request: Request):
    return templates.TemplateResponse(request, "edit_patient-treatment-plan.html")


@router.get("/training-results")
async def page_training_results(request: Request):
    return templates.TemplateResponse(request, "training-results.html")
