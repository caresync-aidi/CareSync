from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import uuid
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from openai import OpenAI
from prometheus_fastapi_instrumentator import Instrumentator
import json
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
MODELS_DIR = os.path.join(BASE_DIR, "models")

app = FastAPI(title="CareSync API")

# Mount frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Load models
recovery_model = joblib.load(os.path.join(MODELS_DIR, "model_recovery.joblib"))
diet_model = joblib.load(os.path.join(MODELS_DIR, "model_diet.joblib"))

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  
) if DATABASE_URL else None

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)

class PredictRequest(BaseModel):
    age: str
    sex: str
    weight: str
    height: str
    condition_type: str
    severity_score: str
    diabetic: str
    exercise: str
    alcohol_units: str
    sleep_hours: str
    medication_adherence: str
    smoking_status: str
    daily_steps: str

def init_db():
    if engine:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS reports (
                    id SERIAL PRIMARY KEY,
                    share_id UUID UNIQUE NOT NULL,
                    inputs JSONB NOT NULL,
                    recovery_days INT,
                    diet_plan TEXT,
                    report_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()

init_db()

@app.get("/")
async def serve_frontend():
    with open(os.path.join(FRONTEND_DIR, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/style.css")
async def serve_css():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(FRONTEND_DIR, "style.css"))

@app.post("/api/predict")
async def predict(req: PredictRequest):

    if not req.age or not req.weight or not req.height:
        raise HTTPException(status_code=400, detail="Missing required fields")
    try:
        # Convert inputs
        inputs = {
            "age": int(req.age),
            "sex": req.sex.capitalize(),
            "weight": float(req.weight),
            "height": float(req.height),
            "condition_type": req.condition_type.capitalize(),
            "severity_score": int(req.severity_score),
            "diabetic": 1 if str(req.diabetic).lower() in ["yes", "1", "true"] else 0,
            "exercise": 1 if str(req.exercise).lower() in ["yes", "1", "true"] else 0,
            "alcohol_units": float(req.alcohol_units),
            "sleep_hours": float(req.sleep_hours),
            "medication_adherence": float(req.medication_adherence),
            "smoking_status": req.smoking_status.capitalize(),
            "daily_steps": float(req.daily_steps)
        }
        
        bmi = inputs["weight"] / (inputs["height"] / 100) ** 2

        # Recovery prediction
        recovery_df = pd.DataFrame([{
            k: inputs[k] for k in ["age", "sex", "weight", "height", "condition_type",
                                   "severity_score", "diabetic", "exercise", "alcohol_units",
                                   "sleep_hours", "medication_adherence", "smoking_status"]
        }])
        recovery_days = int(recovery_model.predict(recovery_df)[0])

        # Diet prediction
        diet_df = pd.DataFrame([{
            "age": inputs["age"],
            "sex": inputs["sex"],
            "bmi": bmi,
            "diabetic": inputs["diabetic"],
            "condition_type": inputs["condition_type"],
            "exercise": inputs["exercise"],
            "alcohol_units": inputs["alcohol_units"],
            "daily_steps": inputs["daily_steps"],
            "sleep_hours": inputs["sleep_hours"]
        }])
        diet_plan = diet_model.predict(diet_df)[0]

        # Generate explainable report with OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""You are a caring health assistant for CareSync.
Patient data: Age {inputs['age']}, Sex {inputs['sex']}, BMI {bmi:.1f}, Condition: {inputs['condition_type']}, Severity: {inputs['severity_score']}/10
Lifestyle: Sleep {inputs['sleep_hours']}hrs/night, Alcohol {inputs['alcohol_units']} units/week, Smoking {inputs['smoking_status']}
Predicted recovery: {recovery_days} days
Recommended diet: {diet_plan}
Generate a warm, easy-to-understand 300-word report. Display the patient data and predicted data. Do not use hashes(#) or asterisk(*), just use numbers(1,2,3...). Do not use this format ,example:**Patient Overview**, it should be Patient Overview, you can use punctuation. Include strict disclaimers that this is NOT medical advice and clearly instruct users to consult medical professionals.
IMPORTANT: Provide immediate, actionable guidance such as hydration advice, safe over-the-counter symptom relief suggestions, and basic exercise/rest recommendations. Explicitly flag any medication conflicts or high-risk habits (like smoking or poor sleep) from the lifestyle data. Use short paragraphs and HTML tags like <br> and <b> for bold headers and bullet points. In the end give a one sentence summary in three lines"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        report_text = response.choices[0].message.content if response.choices else "Report generation failed."

        # Save to NeonDB (if available)
        share_id = uuid.uuid4()
        if engine:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO reports (share_id, inputs, recovery_days, diet_plan, report_text)
                    VALUES (:share_id, :inputs, :recovery_days, :diet_plan, :report_text)
                """), {
                    "share_id": str(share_id),
                    "inputs": json.dumps(inputs),   # ✅ FIXED
                    "recovery_days": recovery_days,
                    "diet_plan": diet_plan,
                    "report_text": report_text
                })
                conn.commit()

        return {
            "recovery_days": recovery_days,
            "diet_plan": diet_plan,
            "report": report_text,
            "share_id": str(share_id)
        }

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
newline = "\n"
@app.get("/report/{share_id}")
async def get_report(share_id: str):
    if not engine:
        raise HTTPException(status_code=404, detail="Database not configured")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM reports WHERE share_id = :id"), {"id": share_id}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Report not found")
        return HTMLResponse(f"""
            <html>
            <head><title>CareSync Report</title>
            <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="p-8 max-w-3xl mx-auto bg-gray-50">
                <h1 class="text-4xl font-bold mb-6 text-center">CareSync Report</h1>
                <div class="bg-white rounded-3xl shadow p-8">
                    <p class="text-emerald-600 text-3xl font-semibold">Recovery Time: {result.recovery_days} days</p>
                    <p class="text-xl mt-2">Recommended Diet: <strong>{result.diet_plan}</strong></p>
                    <div class="prose mt-8 text-gray-700">{result.report_text.replace(newline, '<br>')}</div>
                </div>
                <p class="text-xs text-gray-400 mt-12 text-center">Shared via CareSync • Report ID: {share_id}</p>
            </body>
            </html>
        """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)