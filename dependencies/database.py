import pymongo
from pymongo import AsyncMongoClient


class Database:
    def __init__(self, mongodb_uri: str) -> None:
        client = AsyncMongoClient(mongodb_uri)
        database = client.get_database("Gambly")

        self.users = database.get_collection("users")

    async def register(self, discord_id: int) -> None:
        await self.users.insert_one(
            {
                "discord_id": discord_id,
                "balance": 0
            }
        )

    async def get_balance(self, discord_id: int) -> int:
        user = await self.users.find_one(
            {
                "discord_id": discord_id
            }
        )

        return user["balance"]

    async def set_balance(self, discord_id: int, new_balance: int) -> None:
        await self.users.update_one(
            {
                "discord_id": discord_id
            },
            {
                "$set": {
                    "balance": new_balance
                }
            }
        )

    async def get_leaderboard(self) -> list[tuple[int, int]]:
        cursor = self.users.find() \
            .sort("balance", pymongo.DESCENDING)

        pages = list()

        async for user in cursor:
            pages.append(
                (
                    user["discord_id"],
                    user["balance"]
                )
            )

        return pages
