from asyncio import run

import bakery

from .bakery import Container


async def main() -> None:
    bakery.logger = None
    async with Container():
        notifier = Container().notifier
        await notifier.notify_all()


if __name__ == "__main__":
    run(main())
