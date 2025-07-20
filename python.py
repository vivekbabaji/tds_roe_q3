from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

# Load dataset
with open('q-fastapi-llm-query.json', 'r') as f:
    data = json.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_query(q):
    q = q.lower()
    if "total sales" in q:
        product = None
        city = None
        for word in q.split():
            if word in q:
                if "shirt" in q:
                    product = "Shirt"
                elif "soap" in q:
                    product = "Soap"
                elif "chips" in q:
                    product = "Chips"
                elif "car" in q:
                    product = "Car"
        for item in data:
            if item['city'].lower() in q:
                city = item['city']
        if product and city:
            total = sum(item['sales'] for item in data if item['product'] == product and item['city'] == city)
            return total
        return "Could not find matching product and city in question."
    elif "how many sales reps" in q:
        region = None
        for item in data:
            if item['region'].lower() in q:
                region = item['region']
        if region:
            reps = set()
            for item in data:
                if item['region'] == region:
                    reps.add(item['rep'])
            return len(reps)
        return "Region not found in dataset."
    elif "average sales" in q:
        product = None
        region = None
        if "shirt" in q:
            product = "Shirt"
        elif "soap" in q:
            product = "Soap"
        elif "chips" in q:
            product = "Chips"
        elif "car" in q:
            product = "Car"
        for item in data:
            if item['region'].lower() in q:
                region = item['region']
        if product and region:
            filtered = [item['sales'] for item in data if item['product'] == product and item['region'] == region]
            if filtered:
                return sum(filtered) / len(filtered)
            else:
                return "No data found for this product and region."
        return "Product or region not found."
    elif "highest sale" in q:
        rep = None
        city = None
        for item in data:
            if item['rep'].lower() in q:
                rep = item['rep']
            if item['city'].lower() in q:
                city = item['city']
        if rep and city:
            filtered = [item for item in data if item['rep'] == rep and item['city'] == city]
            if filtered:
                highest = max(filtered, key=lambda x: x['sales'])
                return highest['date']
            else:
                return "No matching sales found for rep and city."
        return "Rep or city not found."
    else:
        return "Query type not supported."

@app.get("/query")
async def query(request: Request, response: Response, q: str):
    answer = process_query(q)
    response.headers["X-Email"] = "23f1001848@ds.study.iitm.ac.in"
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
