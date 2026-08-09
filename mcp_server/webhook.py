from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/webhook")
async def verify_webhook(request: Request):
    return {"status": "verification endpoint working"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    print("Received webhook:")
    print(data)

    return {"status": "received"}