# Diamante Testnet Scripts 🚀

This collection of Python scripts empowers you to interact seamlessly with the Diamante Testnet, a blockchain test network for decentralized applications. The core script, `main.py`, offers automation and multi-account support for core testnet activities.

🔗 Register: [Diamante](https://campaign.diamante.io/?ref=SAC-7AZK)

## ✨ Features Overview

### General Features

- **Multi-Account Support**: Reads private keys from `pvkey.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.

### Included Scripts

1. **Faucet $DIAM**: Automatic daily faucet token DIAM
2. **Transfer**: Automatic Send TX random or File (address.txt)

## 🛠️ Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, `aiohttp_socks` and `inquirer` are included).
- **pvkey.txt**: Add private keys (one per line) for wallet automation.
- **proxies.txt** (optional): Add proxy addresses for network requests, if needed.

## 📦 Installation

1. **Clone this repository:**
   ```sh
   [git clone https://github.com/ephraimcrypto21/diamante.git)
   cd diamante
   cd Diamante-testnet
   ```
2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Prepare Input Files:**
   - Open the `pvkey.txt`: Add your private keys (one per line) in the root directory.
   ```sh
   nano pvkey.txt 
   ```
   - Create `proxies.txt` for specific operations:
   ```sh
   nano proxies.txt
   ```
4. **Run:**
   ```sh
   python main.py
   ```
   - Choose a language (Vietnamese/English).

## 📨 Contact

Connect with us for support or updates:

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 

----

## ☕ Support Us

Love these scripts? Fuel our work with a coffee!

🔗 BUYMECAFE: [BUY ME CAFE](https://buymecafe.vercel.app/)

🔗 WEBSITE: [BUY SCRIPS](https://thogtoolhub.pages.dev/)
