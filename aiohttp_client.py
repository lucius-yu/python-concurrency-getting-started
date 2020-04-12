# fetch multiple urls
# test together with aiohttp_server.py 
import aiohttp
import asyncio

base_url = 'http://127.0.0.1:8080/'

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.text()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url))
        tasks.append(task)
    
    results = []
    while tasks and len(tasks) > 0:
      completed, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
      # fetch result from completed tasks
      results += [t.result() for t in completed]
      print(results)

      # assign pending to tasks, you can cancel pending tasks and breakout if you only want 1 url result
      tasks = pending
      
    return results

async def main():    
    urls = [base_url + 'pear', base_url + 'apple', base_url + 'banana']
    async with aiohttp.ClientSession() as session:
        results = await fetch_all(session, urls)
        print(results)
        

if __name__ == '__main__':
  # use high level api to run 
  asyncio.run(main())

  # or use loop
  # loop = asyncio.get_event_loop()
  # loop.run_until_complete(main())