import aiohttp

from dataclasses import dataclass, make_dataclass

from configs import API_URL


@dataclass
class TgUser:
    tg_id: str
    username: str
    first_name: str
    last_name: str


@dataclass
class UserForcing:
    tg_user: str
    json: dict


async def get_or_create_user(tg_id: str, username: str, first_name: str, last_name: str) -> TgUser:
    async with aiohttp.ClientSession() as session:
        data = {
            "tg_user": tg_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
        async with session.post(API_URL + '/api/tgUser/', json=data) as resp:
            response = await resp.json()
            if response.status == 201:
                user = make_dataclass("TgUser", ['tg_id', 'username', 'first_name', 'last_name'])
                user_obj = user(response['tg_id'],
                                response['username'],
                                response['first_name'],
                                response['last_name'])
                return user_obj


async def upload_updates_to_server(tg_id: str, json: dict) -> UserForcing:
    async with aiohttp.ClientSession() as session:
        data = {
            "tg_user_id": tg_id,
            "json": json
        }
        async with session.post(API_URL + '/api/statUser/', json=data) as resp:
            response = await resp.json()
            if response.status_code == 201:
                forcing = make_dataclass("UserForcing", ['id'])
                forcing_obj = forcing(response['id'])
                return forcing_obj

