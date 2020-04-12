# thumbnail_maker.py
import time
import os
import logging
from urllib.parse import urlparse
from urllib.request import urlretrieve

import PIL
from PIL import Image

# 1. import needed lib
import asyncio
import aiohttp
import aiofiles

FORMAT = "[%(threadName)s, %(asctime)s, %(levelname)s, %(message)s]"
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)


class ThumbnailMakerService(object):
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'

    # 2. download an image asynchronously
    async def download_image_coro(self, session, url):
      img_filename = urlparse(url).path.split('/')[-1]
      img_filepath = self.input_dir + os.path.sep + img_filename

      # download
      async with session.get(url) as response:
        async with aiofiles.open(img_filepath, 'wb') as f:
          logging.debug("await response.content.read for {}".format(url))
          content = await response.content.read()
          logging.debug("await write for {}".format(url))
          await f.write(content)
    
    # 3. batch download coroutine 
    async def download_images_coro(self, img_url_list):
      async with aiohttp.ClientSession() as session:
        '''
        for idx, url in enumerate(img_url_list):
          logging.debug("Start {} coro for downloading {}".format(idx,url))
          await self.download_image_coro(session, url)
        '''
        logging.debug("Start all coros for downloading")
        completed, pending = await asyncio.wait([asyncio.create_task(self.download_image_coro(session, url)) for url in img_url_list])
        logging.info("complete {} download tasks".format(len(completed)))
        
    def download_images(self, img_url_list):
        # validate inputs
        if not img_url_list:
            return
        os.makedirs(self.input_dir, exist_ok=True)
        
        logging.info("beginning image downloads")

        start = time.perf_counter()
        # 4. create loop and call download_images_coro
        loop = asyncio.get_event_loop()
        try:
          loop.run_until_complete(self.download_images_coro(img_url_list))
        finally:
          loop.close()

        end = time.perf_counter()

        logging.info("downloaded {} images in {} seconds".format(len(img_url_list), end - start))

    def perform_resizing(self):
        # validate inputs
        if not os.listdir(self.input_dir):
            return
        os.makedirs(self.output_dir, exist_ok=True)

        logging.info("beginning image resizing")
        target_sizes = [32, 64, 200]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        for filename in os.listdir(self.input_dir):
            orig_img = Image.open(self.input_dir + os.path.sep + filename)
            for basewidth in target_sizes:
                img = orig_img
                # calculate target height of the resized image to maintain the aspect ratio
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                # perform resizing
                img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)
                
                # save the resized image to the output dir with a modified file name 
                new_filename = os.path.splitext(filename)[0] + \
                    '_' + str(basewidth) + os.path.splitext(filename)[1]
                img.save(self.output_dir + os.path.sep + new_filename)

            os.remove(self.input_dir + os.path.sep + filename)
        end = time.perf_counter()

        logging.info("created {} thumbnails in {} seconds".format(num_images, end - start))

    def make_thumbnails(self, img_url_list):
        logging.info("START make_thumbnails")
        start = time.perf_counter()

        self.download_images(img_url_list)
        self.perform_resizing()

        end = time.perf_counter()
        logging.info("END make_thumbnails in {} seconds".format(end - start))
    