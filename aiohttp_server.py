from aiohttp import web

import asyncio

# simulate an slow IO operation
async def get_number(name):
  num = ord(name[0])
  await asyncio.sleep(max(num-97, 0))
  return num

async def handle(request):
  name = request.match_info.get('name',"Anonymous")
  number = await get_number(name)
  text = 'Hello, ' + name + ':' + str(number)
  return web.Response(text=text)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app)