from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rayeva AI Assignment API is running"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_category_tags(monkeypatch):
    from app.services.category_service import CategoryService

    def fake_analyze_product(self, db, payload):
        return SimpleNamespace(
            id=1,
            product_name=payload.product_name,
            primary_category="Kitchenware",
            sub_category="Lunch Boxes",
            seo_tags=["bamboo", "eco-friendly", "reusable", "lunch box", "sustainable"],
            sustainability_filters=["plastic-free", "reusable", "biodegradable"],
        )

    monkeypatch.setattr(CategoryService, "analyze_product", fake_analyze_product)

    payload = {
        "product_name": "Bamboo Fiber Lunch Box",
        "description": "Reusable eco-friendly lunch box made from bamboo fiber.",
        "materials": ["bamboo fiber"],
        "price": 299,
        "target_market": "urban eco-conscious consumers",
    }

    response = client.post("/ai/category-tags", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["product_name"] == "Bamboo Fiber Lunch Box"
    assert data["result"]["primary_category"] == "Kitchenware"
    assert data["result"]["sub_category"] == "Lunch Boxes"
    assert "bamboo" in data["result"]["seo_tags"]
    assert "reusable" in data["result"]["sustainability_filters"]


def test_generate_proposal(monkeypatch):
    from app.services.proposal_service import ProposalService

    def fake_generate_proposal(self, db, payload):
        return SimpleNamespace(
            id=1,
            buyer_name=payload.buyer_name,
            product_mix=[
                {"product": "Recycled Paper Notebooks", "quantity": 100, "allocated_budget": 15000},
                {"product": "Bamboo Pens", "quantity": 200, "allocated_budget": 10000},
            ],
            cost_breakdown={
                "products_total": 25000,
                "packaging": 3000,
                "shipping": 2000,
                "grand_total": 30000,
            },
            impact_positioning_summary="A sustainable office starter pack focused on reducing plastic use and improving eco-brand positioning.",
        )

    monkeypatch.setattr(ProposalService, "generate_proposal", fake_generate_proposal)

    payload = {
        "buyer_name": "GreenKart Retail",
        "budget": 50000,
        "business_type": "retail",
        "goals": ["sustainable gifting", "plastic reduction"],
        "preferred_categories": ["stationery", "packaging", "office supplies"],
    }

    response = client.post("/ai/proposals", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["buyer_name"] == "GreenKart Retail"
    assert len(data["result"]["recommended_product_mix"]) == 2
    assert data["result"]["cost_breakdown"]["grand_total"] == 30000
    assert "sustainable" in data["result"]["impact_positioning_summary"].lower()