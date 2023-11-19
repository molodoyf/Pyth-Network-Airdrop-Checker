import requests
import questionary
from time import sleep
import os

def perform_check(ecosystem: str, wallet: str, proxy: str = None):
    url = f'https://airdrop.pyth.network/api/grant/v1/'

    if ecosystem.lower() == 'evm':
        url += f'evm_breakdown?identity={wallet}'
    elif ecosystem.lower() == 'aptos':
        url += f'amount_and_proof?ecosystem=aptos&identity={wallet}'
    elif ecosystem.lower() == 'sui':
        url += f'amount_and_proof?ecosystem=sui&identity={wallet}'
    elif ecosystem.lower() == 'solana':
        url += f'solana_breakdown?identity={wallet}'
    else:
        raise ValueError(f"Unsupported ecosystem: {ecosystem}")

    if proxy:
        _proxies = {"http": proxy, "https": proxy}
        response = requests.get(url, proxies=_proxies)
    else:
        response = requests.get(url)

    print(response.text)

def get_module():
    modules = [
        {"name": "EVM", "file": "evm.txt", "function": perform_check},
        {"name": "Aptos", "file": "aptos.txt", "function": perform_check},
        {"name": "Sui", "file": "sui.txt", "function": perform_check},
        {"name": "Solana", "file": "solana.txt", "function": perform_check},
    ]

    choices = [f"{i + 1}) {module['name']}" for i, module in enumerate(modules)]

    selected_module_str = questionary.select(
        "Select a method to get started",
        choices=choices,
    ).ask()

    selected_module_index = int(''.join(filter(str.isdigit, selected_module_str)))

    selected_module = modules[selected_module_index - 1]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), selected_module["file"])

    with open(file_path, "r") as file:
        wallets = [w.strip() for w in file]

    with open("proxies.txt", "r") as file:
        proxies = [p.strip() for p in file]

    for i, wallet in enumerate(wallets):
        try:
            selected_module["function"](selected_module["name"].lower(), wallet, proxies[i])
        except IndexError:
            selected_module["function"](selected_module["name"].lower(), wallet)
        except Exception as e:
            print(f'Failed to check wallet {wallet} for {selected_module["name"]}, reason: {e}')
        finally:
            sleep(1)

if __name__ == "__main__":
    get_module()
