import requests
from requests import Response
from os import getenv
from dotenv import load_dotenv

load_dotenv()

base_url = getenv("BASE_URL")


async def get_request_as_json(path: str, headers: dict[str, str] = {}) -> dict[str, any]:
    """
    Get request as json from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as json
    """
    response = await get_request(path, headers)
    return response.json()


async def get_request(path: str, headers: dict[str, str] = {}) -> requests.Response:
    """
    Get request from backend
    :param path api path for request
    :param headers for request, without required
    :return: get response as response object
    """
    return requests.get(
        url=f"{base_url}{path}",
    )


# async def raise_schedule_exception_when_service_unavailable(response: Response):
#     if response.status_code == 503:
#         raise ScheduleServiceUnavailableException
#
#
# async def raise_user_not_found_exception_when_exception_in_response(data):
#     if data["error"]:
#         if data["errorDescription"]["code"] == "UserNotFoundException":
#             raise UserNotFoundException