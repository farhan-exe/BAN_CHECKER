import aiohttp
import asyncio

async def check_ban(uid: str) -> dict | None:
    api_url = f"http://raw.thug4ff.com/check_ban/{uid}"

    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(api_url) as response:
                response.raise_for_status()

                # safer: text load করে তারপর json.loads
                text = await response.text()
                import json
                response_data = json.loads(text)

                if response_data.get("status") == 200:
                    data = response_data.get("data")
                    if data:
                        return {
                            "is_banned": data.get("is_banned", 0),
                            "nickname": data.get("nickname", ""),
                            "period": data.get("period", 0),
                            "region": data.get("region", "")
                        }

                return None

    except aiohttp.ClientError as e:
        print(f"API request failed for UID {uid}: {e}")
        return None

    except asyncio.TimeoutError:
        print(f"API request timed out for UID {uid}.")
        return None

    except Exception as e:
        print(f"Unexpected error for UID {uid}: {e}")
        return None


# Example usage
uid = "7283560779"
data = asyncio.run(check_ban(uid))
print(data)

if data:
    print(f"Nickname: {data['nickname']}, Banned? {data['is_banned']}")
