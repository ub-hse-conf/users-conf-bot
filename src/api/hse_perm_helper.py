from src.api.utils import get_request_as_json


async def get_courses() -> list[int]:
    request_data = await get_request_as_json("available_courses")
    if request_data["error"]:
        return []
    else:
        return request_data["response"]


async def get_programs(course: int) -> list[str]:
    request_data = await get_request_as_json(f"available_programs?course={course}")
    if request_data["error"]:
        return []
    else:
        return request_data["response"]


# расписание - https://api.hse-perm-helper.ru/public/schedule?group=РИС-24-1
# курсы - https://api.hse-perm-helper.ru/public/schedule/available_courses
# программы - https://api.hse-perm-helper.ru/public/schedule/available_programs?course=1
# группы - https://api.hse-perm-helper.ru/public/schedule/available_groups?course=1&program=РИС
