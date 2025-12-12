import os
import sys
import asyncio
import random
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
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, zstd",
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
    "MIN_AMOUNT": 0.00001,
    "MAX_AMOUNT": 999,
    "DEFAULT_AMOUNT": 0.001,
}

LANG = {
    'vi': {
        'title': '✨ DIAMANTE TRANSFER - TESTNET ✨',
        'info': 'ℹ Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'addresses': 'địa chỉ nhận',
        'found_proxies': 'Tìm thấy {count} proxy trong proxies.txt',
        'processing_wallets': '⚙ ĐANG XỬ LÝ {count} VÍ',
        'connecting_wallet': 'Đang kết nối ví...',
        'checking_status': 'Đang kiểm tra trạng thái...',
        'transferring': 'Đang thực hiện transfer...',
        'checking_xp': 'Đang kiểm tra XP...',
        'success': '✅ Transfer thành công!',
        'failure': '❌ Transfer thất bại',
        'wallet_address': 'Địa chỉ ví',
        'to_address': 'Địa chỉ nhận',
        'amount': 'Số lượng',
        'tx_hash': 'TX Hash',
        'tx_status': 'Trạng thái',
        'nonce': 'Nonce',
        'total_xp': 'Tổng XP',
        'current_tx': 'Giao dịch hiện tại',
        'next_badge': 'Badge tiếp theo',
        'mystery_box': 'Mystery Box',
        'user_id': 'User ID',
        'pausing': 'Tạm nghỉ',
        'seconds': 'giây',
        'completed': '✅ HOÀN THÀNH: {successful}/{total} GIAO DỊCH THÀNH CÔNG',
        'error': 'Lỗi',
        'pvkey_not_found': '❌ File pvkey.txt không tồn tại',
        'pvkey_empty': '❌ Không tìm thấy private key hợp lệ',
        'pvkey_error': '❌ Đọc pvkey.txt thất bại',
        'invalid_key': 'không hợp lệ, bỏ qua',
        'address_not_found': '❌ File address.txt không tồn tại',
        'address_empty': '❌ Không tìm thấy địa chỉ nhận hợp lệ',
        'invalid_wallet': 'không hợp lệ, bỏ qua',
        'warning_line': '⚠ Cảnh báo: Dòng',
        'stop_wallet': 'Dừng xử lý ví {wallet}: Quá nhiều giao dịch thất bại liên tiếp',
        'using_proxy': '🔄 Sử dụng Proxy - [{proxy}] với IP công khai - [{public_ip}]',
        'no_proxy': 'Không có proxy',
        'unknown': 'Không xác định',
        'no_proxies': 'Không tìm thấy proxy trong proxies.txt',
        'invalid_proxy': '⚠ Proxy không hợp lệ hoặc không hoạt động: {proxy}',
        'ip_check_failed': '⚠ Không thể kiểm tra IP công khai: {error}',
    },
    'en': {
        'title': '✨ DIAMANTE TRANSFER - TESTNET ✨',
        'info': 'ℹ Info',
        'found': 'Found',
        'wallets': 'wallets',
        'addresses': 'recipient addresses',
        'found_proxies': 'Found {count} proxies in proxies.txt',
        'processing_wallets': '⚙ PROCESSING {count} WALLETS',
        'connecting_wallet': 'Connecting wallet...',
        'checking_status': 'Checking status...',
        'transferring': 'Transferring...',
        'checking_xp': 'Checking XP...',
        'success': '✅ Transfer successful!',
        'failure': '❌ Transfer failed',
        'wallet_address': 'Wallet address',
        'to_address': 'To address',
        'amount': 'Amount',
        'tx_hash': 'TX Hash',
        'tx_status': 'Status',
        'nonce': 'Nonce',
        'total_xp': 'Total XP',
        'current_tx': 'Current transactions',
        'next_badge': 'Next badge',
        'mystery_box': 'Mystery Box',
        'user_id': 'User ID',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': '✅ COMPLETED: {successful}/{total} TRANSACTIONS SUCCESSFUL',
        'error': 'Error',
        'pvkey_not_found': '❌ pvkey.txt file not found',
        'pvkey_empty': '❌ No valid private keys found',
        'pvkey_error': '❌ Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'address_not_found': '❌ address.txt file not found',
        'address_empty': '❌ No valid recipient addresses found',
        'invalid_wallet': 'is invalid, skipped',
        'warning_line': '⚠ Warning: Line',
        'stop_wallet': 'Stopping wallet {wallet}: Too many consecutive failed transactions',
        'using_proxy': '🔄 Using Proxy - [{proxy}] with Public IP - [{public_ip}]',
        'no_proxy': 'None',
        'unknown': 'Unknown',
        'no_proxies': 'No proxies found in proxies.txt',
        'invalid_proxy': '⚠ Invalid or unresponsive proxy: {proxy}',
        'ip_check_failed': '⚠ Failed to check public IP: {error}',
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
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Thêm private keys vào đây, mỗi key trên một dòng\n# Ví dụ: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r', encoding='utf-8') as f:
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

def is_valid_wallet(address: str) -> bool:
    address = address.strip()
    if not address.startswith('0x'):
        return False
    try:
        bytes.fromhex(address.replace('0x', ''))
        return len(address) == 42
    except ValueError:
        return False

def load_addresses(file_path: str = "address.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['address_not_found']}. Sẽ tạo địa chỉ ngẫu nhiên.{Style.RESET_ALL}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Thêm địa chỉ nhận vào đây, mỗi địa chỉ trên một dòng\n# Ví dụ: 0x1234567890abcdef1234567890abcdef12345678\n")
            return []
        
        valid_addresses = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                address = line.strip()
                if address and not address.startswith('#'):
                    if is_valid_wallet(address):
                        valid_addresses.append(address)
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_wallet']}: {address[:10]}...{Style.RESET_ALL}")
        
        if not valid_addresses:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['address_empty']}. Sẽ tạo địa chỉ ngẫu nhiên.{Style.RESET_ALL}")
            return []
        
        return valid_addresses
    except Exception as e:
        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {str(e)}. Sẽ tạo địa chỉ ngẫu nhiên.{Style.RESET_ALL}")
        return []

def load_proxies(file_path: str = "proxies.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Dùng không proxy.{Style.RESET_ALL}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Thêm proxy vào đây, mỗi proxy trên một dòng\n# Ví dụ: socks5://user:pass@host:port hoặc http://host:port\n")
            return []
        
        proxies = []
        with open(file_path, 'r', encoding='utf-8') as f:
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

def generate_random_address() -> str:
    """Tạo địa chỉ Ethereum ngẫu nhiên"""
    random_bytes = bytes([random.randint(0, 255) for _ in range(20)])
    return '0x' + random_bytes.hex()

async def get_proxy_ip(proxy: str = None, language: str = 'en') -> str:
    try:
        if proxy:
            if proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')):
                connector = ProxyConnector.from_url(proxy)
            else:
                parts = proxy.split(':')
                if len(parts) == 4:
                    proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    connector = ProxyConnector.from_url(proxy_url)
                elif len(parts) == 3 and '@' in proxy:
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
    return f"@user{random.randint(10000, 99999)}"

async def transfer_tokens(private_key: str, to_address: str, amount: float, wallet_index: int, proxy: str = None, language: str = 'en'):
    from eth_account import Account
    
    account = Account.from_key(private_key)
    wallet_address = account.address
    
    for attempt in range(CONFIG['MAX_RETRIES']):
        try:
            public_ip = await get_proxy_ip(proxy, language)
            proxy_display = proxy if proxy else LANG[language]['no_proxy']
            print(f"{Fore.CYAN}  🔄 {LANG[language]['using_proxy'].format(proxy=proxy_display, public_ip=public_ip)}{Style.RESET_ALL}")

            device_id = generate_device_id()
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
                    print(f"{Fore.YELLOW}  - {LANG[language]['wallet_address']}: {wallet_address}{Style.RESET_ALL}")
                
                headers_with_token = HEADERS.copy()
                if access_token:
                    headers_with_token['Cookie'] = f"access_token={access_token}"
                
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
                
                if is_social_exists == "INITIAL":
                    print(f"{Fore.CYAN}  > Đăng ký tài khoản...{Style.RESET_ALL}")
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
                        print(f"{Fore.YELLOW}  - Ví testnet: {testnet_wallet}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}  - Social: {social_handle}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}  - Tài khoản đã được đăng ký trước đó{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}  > {LANG[language]['transferring']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  - {LANG[language]['to_address']}: {to_address}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  - {LANG[language]['amount']}: {amount} DIAM{Style.RESET_ALL}")
                
                transfer_payload = {
                    "toAddress": to_address,
                    "amount": amount,
                    "userId": user_id
                }
                
                async with session.post(
                    f"{API_BASE_URL}/transaction/transfer",
                    headers=headers_with_token,
                    json=transfer_payload
                ) as response:
                    if response.status != 200:
                        print(f"{Fore.RED}  ✖ Transfer thất bại: HTTP {response.status}{Style.RESET_ALL}")
                        return False
                    
                    transfer_data = await response.json()
                    if not transfer_data.get('success'):
                        print(f"{Fore.RED}  ✖ Transfer thất bại: {transfer_data.get('message', 'Unknown error')}{Style.RESET_ALL}")
                        return False
                    
                    tx_hash = transfer_data['data']['transferData']['hash']
                    tx_status = transfer_data['data']['transferData']['status']
                    nonce = transfer_data['data']['transferData']['nonce']
                    mystery_box = transfer_data['data'].get('mysteryBoxInfo', {})
                    
                    print(f"{Fore.GREEN}  ✔ {LANG[language]['success']}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['tx_hash']}: {tx_hash}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['tx_status']}: {tx_status}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}  - {LANG[language]['nonce']}: {nonce}{Style.RESET_ALL}")
                    
                    if mystery_box:
                        print(f"{Fore.CYAN}  - {LANG[language]['mystery_box']}: {mystery_box.get('current', 0)}/{mystery_box.get('min', 100)}{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}  > {LANG[language]['checking_xp']}{Style.RESET_ALL}")
                async with session.get(
                    f"{API_BASE_URL}/xp/stats/{user_id}",
                    headers=headers_with_token
                ) as response:
                    if response.status == 200:
                        xp_data = await response.json()
                        if xp_data.get('success'):
                            total_xp = xp_data['data']['totalXP']
                            current_tx = xp_data['data']['currentTransactions']
                            badges = xp_data['data']['badgeHistory']
                            
                            print(f"{Fore.YELLOW}  - {LANG[language]['total_xp']}: {total_xp}{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}  - {LANG[language]['current_tx']}: {current_tx}{Style.RESET_ALL}")
                            
                            # Hiển thị badge tiếp theo
                            for badge in badges:
                                if badge.get('isNextBadge'):
                                    badge_type = badge['badgeType']
                                    progress = badge['progress']
                                    required = badge['requiredTransactions']
                                    print(f"{Fore.CYAN}  - {LANG[language]['next_badge']}: {badge_type} ({progress}/{required}){Style.RESET_ALL}")
                                    break
                
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

async def process_wallet(index: int, wallet_num: int, private_key: str, to_address: str, amount: float, proxy: str, language: str):
    result = await transfer_tokens(private_key, to_address, amount, wallet_num, proxy, language)
    print_separator(Fore.GREEN if result else Fore.RED)
    return result

def print_menu_border(text: str, color=Fore.CYAN):
    """In viền menu đẹp"""
    text = text.strip()
    if len(text) > BORDER_WIDTH - 4:
        text = text[:BORDER_WIDTH - 7] + "..."
    padded_text = f" {text} ".center(BORDER_WIDTH - 2)
    print(f"{color}┌{'─' * (BORDER_WIDTH - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (BORDER_WIDTH - 2)}┘{Style.RESET_ALL}")

def print_menu_option(number: int, text: str):
    """In tùy chọn menu"""
    print(f"    ├─ {Fore.YELLOW}{number}.{Style.RESET_ALL} {Fore.GREEN}{text}{Style.RESET_ALL}")

def print_menu_last_option(number: int, text: str):
    """In tùy chọn cuối cùng của menu"""
    print(f"    └─ {Fore.YELLOW}{number}.{Style.RESET_ALL} {Fore.GREEN}{text}{Style.RESET_ALL}")

def get_user_input(prompt: str, default: str = None, validator=None) -> str:
    """Lấy input từ user với validation"""
    while True:
        if default:
            user_input = input(f"  {Fore.CYAN}> {prompt} (mặc định {default}): {Style.RESET_ALL}").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"  {Fore.CYAN}> {prompt}: {Style.RESET_ALL}").strip()
        
        if validator:
            is_valid, error_msg = validator(user_input)
            if not is_valid:
                print(f"{Fore.RED}  ✖ {error_msg}{Style.RESET_ALL}")
                continue
        
        return user_input

def validate_choice(value: str) -> tuple:
    """Validate lựa chọn 1 hoặc 2"""
    if value not in ['1', '2']:
        return False, "Vui lòng nhập 1 hoặc 2"
    return True, ""

def validate_number(value: str) -> tuple:
    """Validate số nguyên dương"""
    try:
        num = int(value)
        if num <= 0:
            return False, "Số phải lớn hơn 0"
        return True, ""
    except ValueError:
        return False, "Vui lòng nhập số hợp lệ"

def validate_amount(value: str) -> tuple:
    """Validate số lượng DIAM"""
    try:
        amount = float(value)
        if amount < CONFIG['MIN_AMOUNT']:
            return False, f"Số lượng tối thiểu là {CONFIG['MIN_AMOUNT']}"
        if amount > CONFIG['MAX_AMOUNT']:
            return False, f"Số lượng tối đa là {CONFIG['MAX_AMOUNT']}"
        return True, ""
    except ValueError:
        return False, "Vui lòng nhập số hợp lệ"

async def run_transfer(language: str = 'vi'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)

    private_keys = load_private_keys('pvkey.txt', language)
    proxies = load_proxies('proxies.txt', language)

    print(f"{Fore.YELLOW}ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(private_keys)} {LANG[language]['wallets']}{Style.RESET_ALL}")
    print()

    print_menu_border("✦ CHỌN LOẠI GIAO DỊCH")
    print_menu_option(1, "Gửi đến địa chỉ ngẫu nhiên")
    print_menu_last_option(2, "Gửi đến địa chỉ từ file (address.txt)")

    choice = get_user_input("Nhập lựa chọn (1 hoặc 2)", validator=validate_choice)
    print()

    to_addresses = []
    if choice == '2':
        to_addresses = load_addresses('address.txt', language)
        if not to_addresses:
            print(f"{Fore.YELLOW}  ℹ Chuyển sang chế độ gửi đến địa chỉ ngẫu nhiên{Style.RESET_ALL}")
            to_addresses = []

    print_menu_border("✦ NHẬP SỐ LƯỢNG GIAO DỊCH")
    tx_count = int(get_user_input("Số giao dịch", default="1", validator=validate_number))
    print()

    print_menu_border("✦ NHẬP SỐ LƯỢNG DIAM")
    amount = float(get_user_input(
        "Số lượng DIAM",
        default=str(CONFIG['DEFAULT_AMOUNT']),
        validator=validate_amount
    ))
    print()

    if not to_addresses:
        to_addresses = [generate_random_address() for _ in range(tx_count)]
    else:
        while len(to_addresses) < tx_count:
            to_addresses.extend(to_addresses)
        to_addresses = to_addresses[:tx_count]

    successful_transfers = 0
    failed_attempts = 0

    semaphore = asyncio.Semaphore(CONFIG['MAX_CONCURRENCY'])

    async def limited_task(index, wallet_num, private_key, to_addr, proxy):
        nonlocal successful_transfers, failed_attempts
        async with semaphore:
            result = await process_wallet(
                index, wallet_num, private_key, to_addr, amount, proxy, language
            )

            if result:
                successful_transfers += 1
                failed_attempts = 0
            else:
                failed_attempts += 1

            # ✅ FIXED 5-SECOND DELAY BETWEEN TX
            await asyncio.sleep(5)

    # ✅ TASK CREATION (INSIDE run_transfer)
    tasks = []
    task_index = 0

    for w_index, (wallet_num, private_key) in enumerate(private_keys):
        proxy = proxies[w_index % len(proxies)] if proxies else None

        for t in range(tx_count):
            to_addr = to_addresses[t % len(to_addresses)]
            tasks.append(
                limited_task(task_index, wallet_num, private_key, to_addr, proxy)
            )
            task_index += 1

    # ✅ RUN TASKS ONCE
    await asyncio.gather(*tasks, return_exceptions=True)

    print()
    print_border(
        f"{LANG[language]['completed'].format(successful=successful_transfers, total=len(tasks))}",
        Fore.GREEN
    )

