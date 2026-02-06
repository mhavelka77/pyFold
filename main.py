import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse

from pyfold.reference import reference_fold
from pyfold.engine import fold


app = FastAPI()

@app.get("/")
async def get():
    return FileResponse("pyfold/index.html")

@app.post("/generate_reference")
async def generate_reference(request: Request):
    data = await request.json()
    pdb = reference_fold(data['sequence'])
    return JSONResponse({"pdb": pdb})

@app.post("/fold")
async def run_fold(request: Request):
    data = await request.json()
    sequence = data["sequence"]
    steps = data.get("steps", 100)
    return StreamingResponse(fold(sequence, steps), media_type="application/x-ndjson")

def main():
    print("Starting pyFold server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
