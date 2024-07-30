from logging import getLogger, Logger
from fastapi import FastAPI, HTTPException, status

from Docugami.schema import TransformRequest
from hosted_python.service import download_and_get_output_file

logger: Logger = getLogger(__name__)

app = FastAPI()


@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return "Liveness check succeeded."


@app.post("/transform/TakedaICFProcessor", status_code=status.HTTP_204_NO_CONTENT)
async def transform_takeda(request: TransformRequest):
    logger.info(f'DataTransform started on artifact id : {request.artifact.id}')
    try:
        _ = await download_and_get_output_file(request)
    except Exception as e:
        logger.error(f'DataTransform failed on artifact id : {request.artifact.id}\n {e.with_traceback}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DataTransform Failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
