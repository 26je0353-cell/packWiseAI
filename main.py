import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import get_connection, init_db
from .models import RecommendRequest, RecommendResponse, CompareRequest
from .recommendation import recommend_top_materials

app = FastAPI(title="PackWise AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prototype only — restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


def _row_to_material_dict(row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "short_code": row["short_code"],
        "material_form": row["material_form"],
        "oxygen_barrier": row["oxygen_barrier"],
        "moisture_barrier": row["moisture_barrier"],
        "light_barrier": row["light_barrier"],
        "grease_resistance": row["grease_resistance"],
        "mechanical_strength": row["mechanical_strength"],
        "heat_resistance": row["heat_resistance"],
        "cost_level": row["cost_level"],
        "sustainability_level": row["sustainability_level"],
        "recyclable": row["recyclable"],
        "compostable": row["compostable"],
        "data_status": row["data_status"],
    }


def _fetch_all_materials_with_props():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT m.*, p.example_applications, p.advantages, p.limitations
           FROM materials m JOIN material_properties p ON p.material_id = m.id"""
    )
    rows = cur.fetchall()
    conn.close()

    materials = []
    for row in rows:
        d = _row_to_material_dict(row)
        d["example_applications"] = row["example_applications"]
        d["advantages"] = json.loads(row["advantages"])
        d["limitations"] = json.loads(row["limitations"])
        materials.append(d)
    return materials


@app.get("/")
def root():
    return {"status": "ok", "service": "PackWise AI API"}


@app.get("/foods")
def list_foods():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM foods ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/materials")
def list_materials():
    return _fetch_all_materials_with_props()


@app.get("/materials/{material_id}")
def get_material(material_id: int):
    materials = _fetch_all_materials_with_props()
    for m in materials:
        if m["id"] == material_id:
            return m
    raise HTTPException(status_code=404, detail="Material not found")


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    materials = _fetch_all_materials_with_props()
    if not materials:
        raise HTTPException(status_code=500, detail="No materials available")

    food_params = req.model_dump()
    top3 = recommend_top_materials(food_params, materials, top_n=3)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO recommendations (food_id, input_params, result_json) VALUES (?, ?, ?)",
        (req.food_id, json.dumps(food_params), json.dumps(top3)),
    )
    rec_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {"recommendation_id": rec_id, "food_name": req.food_name, "results": top3}


@app.get("/recommend/{recommendation_id}")
def get_recommendation(recommendation_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recommendations WHERE id = ?", (recommendation_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {
        "recommendation_id": row["id"],
        "input_params": json.loads(row["input_params"]),
        "results": json.loads(row["result_json"]),
        "created_at": row["created_at"],
    }


@app.post("/compare")
def compare(req: CompareRequest):
    materials = _fetch_all_materials_with_props()
    by_id = {m["id"]: m for m in materials}
    selected = []
    for mid in req.material_ids:
        if mid not in by_id:
            raise HTTPException(status_code=404, detail=f"Material {mid} not found")
        selected.append(by_id[mid])
    return {"materials": selected}
