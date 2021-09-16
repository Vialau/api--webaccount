import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)

database = client.accounts

accounts_collection = database.get_collection("dev")

# helpers


def accounts_helper(accounts) -> dict:
    return {
        "id": str(accounts["_id"]),
        "firsname": accounts["firstname"],
        "lastname": accounts["lastname"],
        "email": accounts["email"],
        "password": accounts["password"],
    }

# Retrieve all accounts present in the database
async def retrieve_accounts():
    accounts = []
    async for accounts in accounts_collection.find():
        accounts.append(accounts_helper(accounts))
    return accounts


# Add a new account into to the database
async def add_account(account_data: dict) -> dict:
    account = await accounts_collection.insert_one(account_data)
    new_account = await accounts_collection.find_one({"_id": account.inserted_id})
    return accounts_helper(new_account)


# Retrieve an account with a matching ID
async def retrieve_account(id: str) -> dict:
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        return accounts_helper(account)


# Update an account with a matching ID
async def update_account(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        updated_account = await accounts_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_account:
            return True
        return False


# Delete an account from the database
async def delete_account(id: str):
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        await accounts_collection.delete_one({"_id": ObjectId(id)})
        return True