from fastapi import FastAPI,Request,HTTPException
import httpx

app = FastAPI(title="Api gateway")

SERVICES = {
    "auth":"http://localhost:8000",
    # "products":"https://127.0.0.1.8001"
}

client = httpx.AsyncClient()

@app.api_route("/{service}/{rest_of_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_proxy(service: str, rest_of_path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    target_url = f"{SERVICES[service]}/{service}/{rest_of_path}" 
    
    method = request.method
    content = await request.body()
    headers = dict(request.headers)
    
    headers.pop("host", None)

    try:
        response = await client.request(
            method, 
            target_url, 
            content=content, 
            headers=headers, 
            timeout=5.0
        )
        
        return response.json() 
        
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Service {service} is unavailable: {exc}")

@app.get("/health")
def health():
    return {"status": "Gateway is online"}