from sqlite3.dbapi2 import paramstyle

import httpx
#from backend.config import settings


class PolyMarketClient:
    gamma_api = "https://gamma-api.polymarket.com"
    clob_api = "https://clob.polymarket.com"
    def __init__(self):
        #self.gamma_api = settings.POLYMARKET_GAMMA_API_URL
        #self.clob_api = settings.POLYMARKET_GAMMA_API_URL
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
    markets = client.get_markets(limit=5)
    print(f"Fetched {len(markets)} markets")
    for m in markets:
        print(f" - {m.get('question', 'No title')}")
    client.close()