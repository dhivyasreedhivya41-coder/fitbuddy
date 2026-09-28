import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (save_user, save_plan, update_plan,
                          get_original_plan, SessionLocal, User, WorkoutPlan)

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Intha line la thaan main fix irukku
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request,
                     username: str = Form(...),
                     user_id: int = Form(...),
                     age: int = Form(...),
                     weight: float = Form(...),
                     goal: str = Form(...),
                     intensity: str = Form(...)):
    save_user(user_id, username, age, weight, goal, intensity)
    plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
    tip = generate_nutrition_tip_with_flash(goal)
    save_plan(user_id, plan)

    # Ithuvum fix aagirukku
    return templates.TemplateResponse(request=request, name="result.html", context={
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": plan,
        "nutrition_tip": tip
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request,
                    user_id: int = Form(...),
                    feedback: str = Form(...)):
    original = get_original_plan(user_id)
    if not original:
        raise HTTPException(status_code=404, detail="Original plan not found")

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)

    # Ithuvum fix aagirukku
    return templates.TemplateResponse(request=request, name="result.html", context={
        "user_id": user_id,
        "workout_plan": updated,
        "nutrition_tip": "Plan updated based on your feedback!",
        "username": "",
        "age": "",
        "weight": "",
        "goal": "",
        "intensity": ""
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for u in users:
        p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).first()
        user_data.append({
            "id": u.id,
            "name": u.name,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "original_plan": p.original_plan if p else "N/A",
            "updated_plan": p.updated_plan if p and p.updated_plan else "Not updated"
        })
    db.close()
    # Ithuvum fix aagirukku
    return templates.TemplateResponse(request=request, name="all_users.html", context={"users": user_data})