import os
import sys
import asyncio
import random
import json
from colorama import init, Fore, Style
import aiohttp
from aiohttp_socks import ProxyConnector

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền
BORDER_WIDTH = 80

# Constants
API_BASE_URL = "https://campapi.diamante.io/api/v1"
CAMPAIGN_URL = "https://campaign.diamante.io"
IP_CHECK_URL = "https://api.ipify.org?format=json"
MAX_WAIT_TIME = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "Content-Type": "application/json",
    "Origin": CAMPAIGN_URL,
    "Referer": f"{CAMPAIGN_URL}/",
    "sec-ch-ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "access-token": "key"
}

CONFIG = {
    "PAUSE_BETWEEN_ATTEMPTS": [10, 30],
    "MAX_CONCURRENCY": 1,
    "MAX_RETRIES": 3,
    "DEVICE_SOURCE": "web_app",
    "DEVICE_TYPE": "Windows",
    "BROWSERS": ["Chrome", "Edge", "Firefox", "Safari", "Opera"],
}

LANG = {
    'vi': {
        'title': '✨ DIAMANTE FAUCET - TESTNET ✨',
        'info': 'ℹ Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'found_proxies': 'Tìm thấy {count} proxy trong proxies.txt',
        'processing_wallets': '⚙ ĐANG XỬ LÝ {count} VÍ',
        'connecting_wallet': 'Đang kết nối ví...',
        'checking_status': 'Đang kiểm tra trạng thái người dùng...',
        'registering': 'Đăng ký tài khoản...',
        'funding_wallet': 'Đang yêu cầu faucet...',
        'checking_balance': 'Đang kiểm tra số dư...',
        'success': '✅ Claim faucet thành công!',
        'failure': '❌ Claim faucet thất bại',
        'already_registered': 'Tài khoản đã được đăng ký trước đó',
        'wallet_address': 'Địa chỉ ví',
        'testnet_wallet': 'Ví testnet',
        'balance': 'Số dư',
        'funded_amount': 'Số tiền nhận',
        'next_eligible': 'Lần claim tiếp theo',
        'user_id': 'User ID',
        'social_handle': 'Social Handle',
        'referral_code': 'Mã giới thiệu',
        'pausing': 'Tạm nghỉ',
        'seconds': 'giây',
        'completed': '✅ HOÀN THÀNH: {successful}/{total} VÍ THÀNH CÔNG',
        'error': 'Lỗi',
        'pvkey_not_found': '❌ File pvkey.txt không tồn tại',
        'pvkey_empty': '❌ Không tìm thấy private key hợp lệ',
        'pvkey_error': '❌ Đọc pvkey.txt thất bại',
        'invalid_key': 'không hợp lệ, bỏ qua',
        'warning_line': '⚠ Cảnh báo: Dòng',
        'stop_wallet': 'Dừng xử lý ví {wallet}: Quá nhiều giao dịch thất bại liên tiếp',
        'using_proxy': '🔄 Sử dụng Proxy - [{proxy}] với IP công khai - [{public_ip}]',
        'no_proxy': 'Không có proxy',
        'unknown': 'Không xác định',
        'no_proxies': 'Không tìm thấy proxy trong proxies.txt',
        'invalid_proxy': '⚠ Proxy không hợp lệ hoặc không hoạt động: {proxy}',
        'ip_check_failed': '⚠ Không thể kiểm tra IP công khai: {error}',
        'device_id': 'Device ID',
        'ip_address': 'IP Address',
    },
    'en': {
        'title': '✨ DIAMANTE FAUCET - TESTNET ✨',
        'info': 'ℹ Info',
        'found': 'Found',
        'wallets': 'wallets',
        'found_proxies': 'Found {count} proxies in proxies.txt',
        'processing_wallets': '⚙ PROCESSING {count} WALLETS',
        'connecting_wallet': 'Connecting wallet...',
        'checking_status': 'Checking user status...',
        'registering': 'Registering account...',
        'funding_wallet': 'Requesting faucet...',
        'checking_balance': 'Checking balance...',
        'success': '✅ Successfully claimed faucet!',
        'failure': '❌ Failed to claim faucet',
        'already_registered': 'Account already registered',
        'wallet_address': 'Wallet address',
        'testnet_wallet': 'Testnet wallet',
        'balance': 'Balance',
        'funded_amount': 'Funded amount',
        'next_eligible': 'Next eligible at',
        'user_id': 'User ID',
        'social_handle': 'Social Handle',
        'referral_code': 'Referral code',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': '✅ COMPLETED: {successful}/{total} WALLETS SUCCESSFUL',
        'error': 'Error',
        'pvkey_not_found': '❌ pvkey.txt file not found',
        'pvkey_empty': '❌ No valid private keys found',
        'pvkey_error': '❌ Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'warning_line': '⚠ Warning: Line',
        'stop_wallet': 'Stopping wallet {wallet}: Too many consecutive failed transactions',
        'using_proxy': '🔄 Using Proxy - [{proxy}] with Public IP - [{public_ip}]',
        'no_proxy': 'None',
        'unknown': 'Unknown',
        'no_proxies': 'No proxies found in proxies.txt',
        'invalid_proxy': '⚠ Invalid or unresponsive proxy: {proxy}',
        'ip_check_failed': '⚠ Failed to check public IP: {error}',
        'device_id': 'Device ID',
        'ip_address': 'IP Address',
    }
}

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def print_wallets_summary(private_keys: list, language: str = 'en'):
    print_border(
        LANG[language]['processing_wallets'].format(count=len(private_keys)),
        Fore.MAGENTA
    )
    print()

def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

def load_private_keys(file_path: str = "pvkey.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_not_found']}{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Thêm private keys vào đây, mỗi key trên một dòng\n# Ví dụ: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                key = line.strip()
                if key and not key.startswith('#'):
                    if is_valid_private_key(key):
                        if not key.startswith('0x'):
                            key = '0x' + key
                        valid_keys.append((i, key))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_key']}: {key[:10]}...{Style.RESET_ALL}")
        
        if not valid_keys:
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_empty']}{Style.RESET_ALL}")
            sys.exit(1)
        
        return valid_keys
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def load_proxies(file_path: str = "proxies.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Dùng không proxy.{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Thêm proxy vào đây, mỗi proxy trên một dòng\n# Ví dụ: socks5://user:pass@host:port hoặc http://host:port\n")
            return []
        
        proxies = []
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy and not proxy.startswith('#'):
                    proxies.append(proxy)
        
        if not proxies:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Dùng không proxy.{Style.RESET_ALL}")
            return []
        
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['found_proxies'].format(count=len(proxies))}{Style.RESET_ALL}")
        return proxies
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
        return []

async def get_proxy_ip(proxy: str = None, language: str = 'en') -> str:
    try:
        if proxy:
            if proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')):
                connector = ProxyConnector.from_url(proxy)
            else:
                parts = proxy.split(':')
                if len(parts) == 4:  # host:port:user:pass
                    proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    connector = ProxyConnector.from_url(proxy_url)
                elif len(parts) == 3 and '@' in proxy:  # user:pass@host:port
                    connector = ProxyConnector.from_url(f"socks5://{proxy}")
                else:
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['invalid_proxy'].format(proxy=proxy)}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
        else:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
    except Exception as e:
        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=str(e))}{Style.RESET_ALL}")
        return LANG[language]['unknown']

def generate_device_id() -> str:
    return f"DEV{random.randint(1000, 9999)}"

def random_browser() -> str:
    return random.choice(CONFIG['BROWSERS'])

def generate_social_handle() -> str:
    return f"@user{random.randint(1000, 9999)}"

async def claim_faucet(wallet_address: str, wallet_index: int, proxy: str = None, social_handle: str = None, language: str = 'en'):
    for attempt in range(CONFIG['MAX_RETRIES']):
        try:
            public_ip = await get_proxy_ip(proxy, language)
            proxy_display = proxy if proxy else LANG[language]['no_proxy']
            print(f"{Fore.CYAN}  🔄 {LANG[language]['using_proxy'].format(proxy=proxy_display, public_ip=public_ip)}{Style.RESET_ALL}")

            device_id = generate_device_id()
            if not social_handle:
                social_handle = generate_social_handle()
            browser = random_browser()
            
            connector = None
            if proxy:
                if proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')):
                    connector = ProxyConnector.from_url(proxy)
                else:
                    parts = proxy.split(':')
                    if len(parts) == 4:
                        proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                        connector = ProxyConnector.from_url(proxy_url)
            
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=30)) as session:
                # Bước 1: Connect wallet
                print(f"{Fore.CYAN}  > {LANG[language]['connecting_wallet']}{Style.RESET_ALL}")
                connect_payload = {
                    "address": wallet_address,
                    "deviceId": device_id,
                    "deviceSource": CONFIG["DEVICE_SOURCE"],
                    "deviceType": CONFIG["DEVICE_TYPE"],
                    "browser": browser,
                    "ipAddress": public_ip if public_ip != LANG[language]['unknown'] else "0.0.0.0",
                    "latitude": 12.9715987,
                    "longitude": 77.5945627,
                    "countryCode": "Unknown",
                    "country": "Unknown",
                    "continent": "Unknown",
                    "continentCode": "Unknown",
                    "region": "Unknown",
                    "regionCode": "Unknown",
                    "city": "Unknown"
                }
                
                async with session.post(
                    f"{API_BASE_URL}/user/connect-wallet",
                    headers=HEADERS,
                    json=connect_payload
                ) as response:
                    if response.status != 200:
                        print(f"{Fore.RED}  ✖ Kết nối ví thất bại: HTTP {response.status}{Style.RESET_ALL}")
                        return False
                    
                    data = await response.json()
                    if not data.get('success'):
                        print(f"{Fore.RED}  ✖ Kết nối ví thất bại: {data.get('message', 'Unknown error')}{Style.RESET_ALL}")
                        return False
                    
                    user_id = data['data']['userId']
                    access_token = None
                    
                    if 'Set-Cookie' in response.headers or 'set-cookie' in response.headers:
                        cookie_header = response.headers.get('Set-Cookie') or response.headers.get('set-cookie')
                        if 'access_token=' in cookie_header:
                            access_token = cookie_header.split('access_token=')[1].split(';')[0]
                    
                    print(f"{Fore.GREEN}  ✔ Kết nối ví thành công!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['user_id']}: {user_id}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['testnet_wallet']}: {testnet_wallet}{Style.RESET_ALL}")
                
                headers_with_token = HEADERS.copy()
                if access_token:
                    headers_with_token['Cookie'] = f"access_token={access_token}"
                
                # Bước 2: Check user status
                print(f"{Fore.CYAN}  > {LANG[language]['checking_status']}{Style.RESET_ALL}")
                async with session.get(
                    f"{API_BASE_URL}/auth/get-user-status/{user_id}",
                    headers=headers_with_token
                ) as response:
                    if response.status != 200:
                        print(f"{Fore.RED}  ✖ Kiểm tra trạng thái thất bại: HTTP {response.status}{Style.RESET_ALL}")
                        return False
                    
                    status_data = await response.json()
                    is_social_exists = status_data['data']['isSocialExists']
                    
                    print(f"{Fore.YELLOW}  - Trạng thái: {is_social_exists}{Style.RESET_ALL}")
                
                # Bước 3: Register nếu chưa đăng ký
                if is_social_exists == "INITIAL":
                    print(f"{Fore.CYAN}  > {LANG[language]['registering']}{Style.RESET_ALL}")
                    register_payload = {
                        "userId": user_id,
                        "walletAddress": wallet_address,
                        "socialHandle": social_handle,
                        "referralCode": "SAC-7AZK"
                    }
                    
                    async with session.post(
                        f"{API_BASE_URL}/auth/register",
                        headers=headers_with_token,
                        json=register_payload
                    ) as response:
                        if response.status != 200:
                            print(f"{Fore.RED}  ✖ Đăng ký thất bại: HTTP {response.status}{Style.RESET_ALL}")
                            return False
                        
                        register_data = await response.json()
                        if not register_data.get('success'):
                            print(f"{Fore.RED}  ✖ Đăng ký thất bại: {register_data.get('message', 'Unknown error')}{Style.RESET_ALL}")
                            return False
                        
                        testnet_wallet = register_data['data']['testnetWallet']
                        print(f"{Fore.GREEN}  ✔ Đăng ký thành công!{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}  - {LANG[language]['testnet_wallet']}: {testnet_wallet}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}  - {LANG[language]['social_handle']}: {social_handle}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}  - {LANG[language]['already_registered']}{Style.RESET_ALL}")
                
                # Bước 4: Fund wallet
                print(f"{Fore.CYAN}  > {LANG[language]['funding_wallet']}{Style.RESET_ALL}")
                async with session.get(
                    f"{API_BASE_URL}/transaction/fund-wallet/{user_id}",
                    headers=headers_with_token
                ) as response:
                    if response.status != 200:
                        print(f"{Fore.RED}  ✖ Yêu cầu faucet thất bại: HTTP {response.status}{Style.RESET_ALL}")
                        return False
                    
                    fund_data = await response.json()
                    if not fund_data.get('success'):
                        print(f"{Fore.RED}  ✖ Yêu cầu faucet thất bại: {fund_data.get('message', 'Unknown error')}{Style.RESET_ALL}")
                        return False
                    
                    funded_amount = fund_data['data']['fundedAmount']
                    final_balance = fund_data['data']['finalBalance']
                    next_eligible = fund_data['data']['nextEligibleAt']
                    
                    print(f"{Fore.GREEN}  ✔ {LANG[language]['success']}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['funded_amount']}: {funded_amount}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['balance']}: {final_balance}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['next_eligible']}: {next_eligible}{Style.RESET_ALL}")
                
                # Bước 5: Check balance
                print(f"{Fore.CYAN}  > {LANG[language]['checking_balance']}{Style.RESET_ALL}")
                async with session.get(
                    f"{API_BASE_URL}/transaction/get-balance/{user_id}",
                    headers=headers_with_token
                ) as response:
                    if response.status == 200:
                        balance_data = await response.json()
                        if balance_data.get('success'):
                            balance = balance_data['data']['balance']
                            address = balance_data['data']['address']
                            print(f"{Fore.YELLOW}  - {LANG[language]['testnet_wallet']}: {address}{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}  - {LANG[language]['balance']}: {balance}{Style.RESET_ALL}")
                
                return True

        except Exception as e:
            if attempt < CONFIG['MAX_RETRIES'] - 1:
                delay = random.uniform(5, 15)
                print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  ⚠ {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)
                continue
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
            return False

async def process_wallet(index: int, wallet_num: int, wallet_address: str, proxy: str, social_handle: str, language: str):
    result = await claim_faucet(wallet_address, wallet_num, proxy, social_handle, language)
    print_separator(Fore.GREEN if result else Fore.RED)
    return result

async def run_faucet(language: str = 'vi'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)
    print()

    wallets = load_wallets('wallets.txt', language)
    proxies = load_proxies('proxies.txt', language)
    socials = load_social_handles('socials.txt', language)
    print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(wallets)} {LANG[language]['wallets']}{Style.RESET_ALL}")
    print()

    if not wallets:
        return

    successful_claims = 0
    total_wallets = len(wallets)
    failed_attempts = 0
    CONFIG['TOTAL_WALLETS'] = total_wallets
    CONFIG['MAX_CONCURRENCY'] = min(CONFIG['MAX_CONCURRENCY'], total_wallets)

    print_wallets_summary(wallets, language)

    random.shuffle(wallets)
    semaphore = asyncio.Semaphore(CONFIG['MAX_CONCURRENCY'])
    async def limited_task(index, wallet_num, wallet_address, proxy, social_handle):
        nonlocal successful_claims, failed_attempts
        async with semaphore:
            result = await process_wallet(index, wallet_num, wallet_address, proxy, social_handle, language)
            if result:
                successful_claims += 1
                failed_attempts = 0
            else:
                failed_attempts += 1
                if failed_attempts >= 3:
                    print(f"{Fore.RED}  ✖ {LANG[language]['stop_wallet'].format(wallet=wallet_num)}{Style.RESET_ALL}")
                    return
            if index < total_wallets - 1:
                delay = random.uniform(CONFIG['PAUSE_BETWEEN_ATTEMPTS'][0], CONFIG['PAUSE_BETWEEN_ATTEMPTS'][1])
                print(f"{Fore.YELLOW}  ℹ {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)

    tasks = []
    for i, (wallet_num, wallet_address) in enumerate(wallets):
        proxy = proxies[i % len(proxies)] if proxies else None
        social_handle = socials[i % len(socials)] if socials else None
        tasks.append(limited_task(i, wallet_num, wallet_address, proxy, social_handle))

    await asyncio.gather(*tasks, return_exceptions=True)

    print()
    print_border(
        f"{LANG[language]['completed'].format(successful=successful_claims, total=total_wallets)}",
        Fore.GREEN
    )
    print()

if __name__ == "__main__":
    asyncio.run(run_faucet('vi'))
