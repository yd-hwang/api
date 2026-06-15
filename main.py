from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# 모든 GET 요청 차단 (405 Method Not Allowed)
@app.middleware("http")
async def block_get_requests(request: Request, call_next):
    if request.method == "GET":
        return JSONResponse(
            status_code=405,
            content={"detail": "GET method is not allowed. Use POST instead."}
        )
    return await call_next(request)

# 상수 설정
API_KEY = "suwon_univ_2026_api_key"
X_STUDENT_ID = "20201234"

# JSON 데이터 모델 (정확히 2개의 파라미터)
class StudentData(BaseModel):
    name: str
    course: str

@app.post("/api/submit")
async def submit_data(
    data: StudentData,
    x_api_key: str = Header(None, alias="X-API-KEY"),
    x_student_id: str = Header(None, alias="X-STUDENT-ID")
):
    # 두 헤더 모두 필수 검증
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or Missing API Key")
    if not x_student_id or x_student_id != X_STUDENT_ID:
        raise HTTPException(status_code=401, detail="Invalid or Missing Student ID")

    # 정상 요청 처리 (JSON 응답)
    return {
        "status": "success",
        "message": f"{data.name}님, {data.course} 수업 API 연습 성공입니다.",
        "received": {
            "student_id": x_student_id,
            "name": data.name,
            "course": data.course
        }
    }
