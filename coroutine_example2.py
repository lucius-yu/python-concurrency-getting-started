# demo coroutine chain
import asyncio

async def perform_task():
  print("performing task")
  print("waiting for result1")
  result1 = await subtask1()
  print("waiting for result2")
  result2 = await subtask2()
  return(result1, result2)

async def subtask1():
  await asyncio.sleep(2)
  print("performed subtask1")
  return "result1"

async def subtask2():
  await asyncio.sleep(1)
  print("performed subtask2")
  return "result2"

loop = asyncio.get_event_loop()
result = loop.run_until_complete(perform_task())
loop.close()