# parallel coroutine examples

import asyncio

async def get_item(i):
  print("in get_item coroutine and await for getting item {}".format(i))
  await asyncio.sleep(i)
  print("in get_item coroutine and continue after getting item {} happened".format(i))
  return 'item ' + str(i)

async def get_items(num_items):
  print('in get_items corountine')
  item_coros = list()
  for i in range(1,num_items+1):
    print("in get_items corountine and get item {}".format(i))
    coro = get_item(i)
    print("in get_items coroutine and continue")
    item_coros.append(coro)
  print('waiting for tasks to complete')
  # wait for all get_item tasks, some tasks will not be completed when set timeout as 2
  completed, pending = await asyncio.wait(item_coros, timeout=2)
  results = [t.result() for t in completed]
  print('results: {!r}'.format(results))

  if (pending):
    print("cancelling pending tasks")
    for t in pending:
      t.cancel()


loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(get_items(4))
finally:
  loop.close()