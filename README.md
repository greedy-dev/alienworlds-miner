# Alien Worlds Automatic Miner

### A Python script made to automate mining on Alien Worlds

This script:
- Automatically opens the browser
- Automatically logs in (only Reddit accounts supported for now)
- Automatically mines and claims
- Automatically solves captcha
- Prevents being detected as a bot

---

### Requirements
- Python 3.7 or greater
- Chromedriver
- Brave browser
- Installed dependencies from requirements.txt
- [anti-captcha.com](http://getcaptchasolution.com/l5hst1crpb) account
- A Wax.io account
- For automatic login:
  - Wax.io account should be created using Reddit

---

## Installation guide

### Clone this repo
1. Open Terminal (macOS) / cmd (Windows)
2. Use the command `cd path`, instead of `path` type the path where you want the script to be located.
3. Use the command `git clone https://github.com/greedy-dev/alienworlds-miner.git`

### Install Python and dependencies
*Skip this if you already have Python and the required dependencies installed*
1. Install [Python](https://www.python.org/downloads/release/python-395/)
   - If you're on Windows, be sure to check **Add Python to PATH** <br /> ![Checkbox](https://i.imgur.com/uF9TKnU.jpg)
2. Open your Terminal (for macOS) / cmd (for Windows)
3. Use the command `cd path/to/the/script`, replace `path/to/the/script` with the actual path to the folder where the script is located
4. Type `python -m venv venv` to create the virtual environment
5. Activate the virtual environment
    - macOS: Use the command `source venv/bin/activate`
    - Windows: Use the command `venv\Scripts\activate`
6. Install the dependencies by typing `pip3 install -r requirements.txt`

### Install and configure anticaptcha
1. Create an account [here](http://getcaptchasolution.com/l5hst1crpb), make a deposit (1000 solved captchas cost around 2-3 USD), copy API key, you'll need it later.
2. Download [Extensions](https://dropover.cloud/7e74f665dc8bef23ca0a58776a812f5a), move them to the folder with the script files
3. Open `Extensions/anticaptcha/0.52_0/js/config_ac_api_key.js` and replace `your_api_key` on the 3rd line with your anti-captcha API key. Save the file.

### Install other required packages
1. Install [Brave Browser](https://brave.com)
   - macOS: Move Brave Browser.app to the folder with the script
   - Windows: Proceed with regular installation
2. Download [Chromedriver](https://chromedriver.chromium.org/downloads), move it to the folder with the script.
---
## Running the script
1. Open Terminal (macOS) / cmd (Windows)
2. Use the command `cd path/to/the/script`, replace `path/to/the/script` with the actual path to the folder where the script is located
3. Activate the virtual environment
    - macOS: Use the command `source venv/bin/activate`
    - Windows: Use the command `venv\Scripts\activate`
4. Type the command `python main.py` and add the arguments depending on login method (see below)

###Available arguments

| Argument                | Value                | Default | Required?                            | Description                                                                                                                                                              |
|:-----------------------:|:--------------------:|:-------:|:------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--method`              | `reddit` or `manual` | -       | Yes                                  | Login method. <br /> If reddit is selected, the login is automatic. <br /> If manual is selected, you have 60 seconds to log in.                                         |
| `--login`               | String               | -       | If `reddit` login method is selected | Your Reddit username.                                                                                                                                                    |
| `--pw`                  | String               | -       | If `reddit` login method is selected | Your Reddit password.                                                                                                                                                    |
| `--set-mining-timeout`  | Int                  | 300     | No                                   | Resets mining by reloading the website if it took longer than specified amount (in seconds).                                                                             |
| `--set-mining-cooldown` | Int                  | 300     | No                                   | Cooldown between mining cycles in seconds (used if the script was unable to get this from website logs).                                                                 |
| `--mac`                 | Bool                 | False   | No                                   | If specified, macOS executables' paths will be used. No value needs to be provided, just the argument.  By default, Windows executables' paths will be used.             |
| `--debug`               | Bool                 | False   | No                                   | If specified, debug log will be output. By default, the level is INFO.                                                                                                   |

### To run several accounts, open another terminal window and repeat the steps.

---

### *Any problems? [Submit an issue](https://github.com/greedy-dev/alienworlds-miner/issues/new)*


## Donations

WAX: `greedydev.gm`

USDT (TRC20): `TD7TqnCdj4zF2nF38pFAimMcU7uxKSm9Lf`

BTC: `bc1qn9tnlns5nzsl2j4ccy2e6s498303ae8r880g79`

ETH: `0xd4540ac00d1db01818a93c279ae66bc3d18ac8a5`

TRX: `TB2MEHPELhDjL5KRsLqku1CMA5xqhoU2DZ`

ADA: `DdzFFzCqrht3D8nMzFqFMXtvABwoYtyT3nfYv7MG4Vts8Dbuo33KtSkzRhaUV4RAL8qzqjCHpM5Ugj2QjpMPQqDkJXPeF3MY6aSY6sdG`