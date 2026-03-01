import asyncio


async def send_sms(phone: str, message: str) -> None:
    await asyncio.sleep(0.2)


async def send_email(email: str, subject: str, body: str) -> None:
    await asyncio.sleep(0.3)
