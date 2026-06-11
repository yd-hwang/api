from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# API KEY 설정 (수업용 고정값)
API_KEY = "suwon_univ_2026_api_key"

# JSON 데이터 모델 (3개의 파라미터)
class StudentData(BaseModel):
    student_id: str
    name: str
    course: str

@app.post("/api/submit")
async def submit_data(
    data: StudentData,
    x_api_key: str = Header(None, alias="X-API-KEY")
):
    # API KEY 검증
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or Missing API Key")
    
    # 정상 요청 처리 (JSON 응답)
    return {
        "status": "success",
        "message": "데이터가 성공적으로 수신되었습니다.",
        "received_data": {
            "student_id": data.student_id,
            "name": data.name,
            "course": data.course
        }
    }

@app.get("/")
async def root():
    return {"message": "웹 크롤링 수업용 API 서버가 정상 작동 중입니다."}
