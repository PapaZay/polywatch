from fastapi import APIRouter

from services.polymarket_service import PolyMarketClient

router = APIRouter()
client = PolyMarketClient()

@router.get("/markets")
def get_markets(limit: int = 20):
    events = client.get_events(limit=limit)
    markets = []
    for event in events:
        tags = event.get("tags", [])
        category = tags[0]["label"] if tags else None
        for market in event.get("markets", []):
            markets.append({
                "id": market.get("id"),
                "question": market.get("question"),
                "category": category.title() if category else None,
                "volume": market.get("volume"),
                "outcomePrices": market.get("outcomePrices"),
            })
    return markets