from fastapi import APIRouter, UploadFile, File, HTTPException
from ..controllers.emotion_controller import predict_emotion

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = predict_emotion(contents, filename=file.filename)
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
