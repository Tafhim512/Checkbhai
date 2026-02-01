from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, auth
from .database import engine, get_db
from .scam_detector import ScamDetector

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CheckBhai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = ScamDetector()

@app.post("/api/register")
def register(phone: str, name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone == phone).first()
    if user:
        token = auth.create_access_token(data={"sub": user.phone})
        return {"access_token": token, "user": {"phone": user.phone, "name": user.name, "credits": user.credits}}
    
    user = models.User(phone=phone, name=name, credits=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = auth.create_access_token(data={"sub": user.phone})
    return {"access_token": token, "user": {"phone": user.phone, "name": user.name, "credits": user.credits}}

@app.post("/api/check")
def check_scam(text: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check credits
    if current_user and current_user.credits <= 0:
        raise HTTPException(status_code=402, detail="No credits remaining. Please purchase more checks.")
    
    # Analyze
    result = detector.analyze(text)
    
    # Save to database
    check = models.ScamCheck(
        user_id=current_user.id if current_user else None,
        submitted_text=text,
        language=result['language'],
        payment_method_mentioned=result['payment_method_mentioned'],
        risk_level=result['risk_level'],
        risk_score=result['risk_score'],
        red_flags=result['red_flags'],
        ai_analysis=result['ai_analysis'],
        rule_based_flags=result['rule_based_flags'],
        status="analyzed",
        payment_status="free" if (current_user and current_user.credits > 0) else "pending"
    )
    db.add(check)
    
    # Deduct credit
    if current_user:
        current_user.credits -= 1
    
    db.commit()
    db.refresh(check)
    
    return {
        "id": check.id,
        "risk_level": check.risk_level,
        "risk_score": check.risk_score,
        "red_flags": check.red_flags,
        "analysis": check.ai_analysis,
        "language": check.language,
        "payment_method": check.payment_method_mentioned
    }

@app.post("/api/feedback")
def submit_feedback(check_id: int, feedback: str, db: Session = Depends(get_db)):
    check = db.query(models.ScamCheck).filter(models.ScamCheck.id == check_id).first()
    if check:
        check.user_feedback = feedback
        
        # Add to training data if feedback is inaccurate
        if feedback == "inaccurate":
            check.status = "pending_review"
        
        db.commit()
    return {"success": True}

@app.get("/api/history")
def get_history(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    checks = db.query(models.ScamCheck).filter(models.ScamCheck.user_id == current_user.id).order_by(models.ScamCheck.check_date.desc()).limit(20).all()
    return checks

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_checks = db.query(models.ScamCheck).count()
    scams_detected = db.query(models.ScamCheck).filter(models.ScamCheck.risk_level == "high").count()
    
    return {
        "total_checks": total_checks,
        "scams_detected": scams_detected,
        "users_protected": db.query(models.User).count()
    }

# Admin endpoint - manual review
@app.get("/api/admin/pending")
def get_pending_reviews(db: Session = Depends(get_db)):
    return db.query(models.ScamCheck).filter(models.ScamCheck.status == "pending_review").all()

@app.post("/api/admin/review/{check_id}")
def manual_review(check_id: int, correct_label: str, notes: str, db: Session = Depends(get_db)):
    check = db.query(models.ScamCheck).filter(models.ScamCheck.id == check_id).first()
    if check:
        check.status = "reviewed"
        check.manual_review_notes = notes
        
        # Add to training data
        training = models.TrainingData(
            text=check.submitted_text,
            label=correct_label,
            category="other",
            language=check.language,
            source="manual_review",
            verified=True
        )
        db.add(training)
        db.commit()
    
    return {"success": True}
