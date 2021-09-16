from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    add_account,
    delete_account,
    retrieve_account,
    retrieve_accounts,
    update_account,
)
from ..models.account import (
    ErrorResponseModel,
    ResponseModel,
    AccountSchema,
    UpdateAccountModel,
)

router = APIRouter()


# Create an account

@router.post("/", response_description="Account data added into the database")
async def add_account_data(account: AccountSchema = Body(...)):
    account = jsonable_encoder(account)
    new_account = await add_account(account)
    return ResponseModel(new_account, "Account added successfully.")

# GET accounts

@router.get("/", response_description="Accounts retrieved")
async def get_accounts():
    accounts = await retrieve_accounts()
    if accounts:
        return ResponseModel(accounts, "Accounts data retrieved successfully")
    return ResponseModel(accounts, "Empty list returned")

# GET account by ID

@router.get("/{id}", response_description="Account data retrieved")
async def get_account_data(id):
    account = await retrieve_account(id)
    if account:
        return ResponseModel(account, "Account data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Account doesn't exist.")

# Update account by ID

@router.put("/{id}")
async def update_account_data(id: str, req: UpdateAccountModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_account = await update_account(id, req)
    if updated_account:
        return ResponseModel(
            "Account with ID: {} update is successful".format(id),
            "Account updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the account data.",
    )

# Delete an account

@router.delete("/{id}", response_description="Account data deleted from the database")
async def delete_account_data(id: str):
    deleted_account = await delete_account(id)
    if deleted_account:
        return ResponseModel(
            "Account with ID: {} removed".format(id), "Account deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Account with id {0} doesn't exist".format(id)
    )