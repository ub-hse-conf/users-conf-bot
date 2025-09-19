from aiohttp import web

async def health(request):
    try:
        bot = request.app["bot"]
        await bot.get_me()
        return web.json_response({"status": "ok", "bot": "running"})
    except Exception as e:
        return web.json_response({"status": "error", "reason": str(e)}, status=500)