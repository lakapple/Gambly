from pymongo import AsyncMongoClient


class Database:
    def __init__(self, uri: str):
        client = AsyncMongoClient(uri)
        database = client.get_database("gambly")

        self.users = database.get_collection("users")

    async def register_user(self, discord_id: int):
        await self.users.insert_one(
            {
                "discord_id": discord_id,
                "balance": 0,
            }
        )

    async def set_balance(self, discord_id: int, new_balance: int):
        await self.users.update_one(
            {
                "discord_id": discord_id,
            },
            {
                "balance": new_balance,
            }
        )

    async def get_balance(self, discord_id: int) -> int:
        user = await self.users.find_one(
            {
                "discord_id": discord_id,
            }
        )

        print(user)
