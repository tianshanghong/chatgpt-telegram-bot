from typing import Dict, List
import aiohttp
from .plugin import Plugin


class OlynCollector(Plugin):
    """
    A plugin to fetch the status of all Olyn recycling collectors
    """

    def get_source_name(self) -> str:
        return "OlynCollector"

    def get_spec(self) -> List[Dict]:
        return [{
            "name": "get_all_collectors",
            "description": "Get the status of all Olyn recycling collectors. Note: If a collector's "
                           "operational_status is 'needs-maintenance', inform the user not to make a trip there.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }]

    async def execute(self, function_name: str, helper, **kwargs) -> Dict:
        if function_name == "get_all_collectors":
            return await self._get_all_collectors()
        else:
            raise ValueError(f"Unknown function: {function_name}")

    async def _get_all_collectors(self) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.olyns.com/api/collectors") as response:
                data = await response.json()

        collectors = data.get("collectors", [])

        result = {
            "collectors": [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "status": c["status"],
                    "operational_status": c["operational_status"],
                    "address": c["address"],
                    "latitude": c["latitude"],
                    "longitude": c["longitude"],
                    "bin_status": c["bin_status"],
                    "bin_levels": c["bin_levels"],
                }
                for c in collectors
            ]
        }

        return result
