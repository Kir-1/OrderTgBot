import os
import random

from aiogram.types import FSInputFile


async def take_photo() -> FSInputFile:
    directory = './source/pic'
    photo_name = random.choice(os.listdir(directory))
    return FSInputFile(path=os.path.join(directory, photo_name), filename=photo_name)

