import httpx
from config import settings


class PolyMarketClient:
    #gamma_api = "https://gamma-api.polymarket.com"
    #clob_api = "https://clob.polymarket.com"
    def __init__(self):
        self.gamma_api = settings.POLYMARKET_GAMMA_API_URL
        self.clob_api = settings.POLYMARKET_CLOB_API_URL
        self.client = httpx.Client(timeout=30)

    def get_markets(self, limit: int = 100, offset: int = 0, closed: bool = False) -> list:
        response = self.client.get(f"{self.gamma_api}/markets",
                                   params={"limit": limit, "offset": offset, "closed": closed}
                                   )
        response.raise_for_status()
        return response.json()

    def get_events(self, limit: int = 100, closed: bool = False) -> list:
        response = self.client.get(f"{self.gamma_api}/events",
                                   params={"limit": limit, "closed": closed}
                                   )
        response.raise_for_status()
        return response.json()

    def get_prices(self, token_id: str) -> dict:
        response = self.client.get(f"{self.clob_api}/price", params={"token_id": token_id})
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()

if __name__ == "__main__":
    client = PolyMarketClient()
    try:
        events = client.get_events(limit=5)
        print(f"Fetched {len(events)} events")
        for e in events:
            print(f" - {e.get('title', 'No title')}")
    except Exception as e:
        print(f"Error {e}")
    finally:
        client.close()