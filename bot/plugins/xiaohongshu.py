import os
from typing import Dict, List
import aiohttp
from .plugin import Plugin

class XiaohongshuPlugin(Plugin):
    """
    A plugin to fetch data from Xiaohongshu (小红书) to help with shopping and travel decisions.
    """
    def __init__(self):
        self.api_key = os.getenv('XIAOHONGSHU_API_KEY')
        if not self.api_key:
            raise ValueError('XIAOHONGSHU_API_KEY environment variable must be set to use Xiaohongshu Plugin')
        self.api_base = 'https://apiok.us/api/0eab'

    def get_source_name(self) -> str:
        return "Xiaohongshu"

    def get_spec(self) -> List[Dict]:
        return [
            {
                "name": "get_note_details",
                "description": "Get details of a specific note from Xiaohongshu",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "note_id": {
                            "type": "string",
                            "description": "The ID of the note to fetch details for"
                        }
                    },
                    "required": ["note_id"]
                }
            },
            {
                "name": "search_notes",
                "description": "Search for notes on Xiaohongshu based on keywords",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "page_id": {
                            "type": "string",
                            "description": "The page ID for pagination (optional)"
                        },
                        "sort_type": {
                            "type": "integer",
                            "description": "Sort type: 0 (综合), 1 (最热), 2 (最新) (optional)"
                        },
                        "filter_note_type": {
                            "type": "integer",
                            "description": "Filter note type: 0 (默认), 1 (视频筛选), 2 (图文筛选) (optional)"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        if function_name == "get_note_details":
            return await self._get_note_details(**kwargs)
        elif function_name == "search_notes":
            return await self._search_notes(**kwargs)
        else:
            raise ValueError(f"Unknown function: {function_name}")

    async def _get_note_details(self, note_id: str) -> Dict:
        url = f"{self.api_base}/note/detail/v1"
        params = {
            "apikey": self.api_key,
            "note_id": note_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=60) as response:
                data = await response.json()
                if data['code'] != 0:
                    raise Exception(f"Xiaohongshu API error: {data.get('msg') or data.get('tip') or 'Unknown error'}")
                return data['result']

    async def _search_notes(self, query: str, page_id: str = None, sort_type: int = None, filter_note_type: int = None) -> Dict:
        url = f"{self.api_base}/search/notes/v1"
        params = {
            "apikey": self.api_key,
            "query": query
        }
        if page_id:
            params["page_id"] = page_id
        if sort_type is not None:
            params["sort_type"] = sort_type
        if filter_note_type is not None:
            params["filter_note_type"] = filter_note_type

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=60) as response:
                data = await response.json()
                if data['code'] != 0:
                    raise Exception(f"Xiaohongshu API error: {data.get('msg') or data.get('tip') or 'Unknown error'}")
                return data['result']
