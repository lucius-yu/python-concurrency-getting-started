import asyncio

async def delayed_hello():
  print("Hello, ")
  # await will pause this coroutine until event happen
  await asyncio.sleep(1)
  print("World!")

loop = asyncio.get_event_loop()
# delay_hello will return a coroutine object
# in run_until_compolete, returned coroutine object will be wrappered as future object
loop.run_until_complete(delayed_hello()) 
print("say_hello complete")
loop.close()