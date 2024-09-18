import asyncio, os
from DB.sql import create_database
from settings import DEFAULT_VLESS_FILE
from xray_service.utils import get_default_vless


async def add_client(tlg_id: int) -> bool:
    # create database
    await create_database()

    # get default vless
    # set vless params

    # create client
    # save client
    # get enabled clients

    # copy last vless file
    # save new vless file
    # restart xray
    # check status
    # recovery if error

    pass


if __name__ == "__main__":
    asyncio.run(add_client(123))