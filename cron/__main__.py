from asyncio import run

from .bakery import Container


async def main() -> None:
    async with Container():
        notifier = Container().notifier
        await notifier.notify_all()


if __name__ == "__main__":
    run(main())
