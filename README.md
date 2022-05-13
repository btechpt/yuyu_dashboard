# Yuyu

## Setup

Make sure you know where Horizon is located

Run this command

```bash
./setup_yuyu.sh
```

Enter horizon location and press ENTER.

Activate Horzon Virtual Environment if exist.

Install Yuyu Dashboard Depencencies with

```
pip3 install -r requirements.txt
```

Add this config to your horizon `local_settings.py`

```bash
YUYU_URL="http://yuyu_server_url:8182"
CURRENCIES = ('IDR', 'USD')
DEFAULT_CURRENCY = "IDR"
```

Then restart Horizon.
