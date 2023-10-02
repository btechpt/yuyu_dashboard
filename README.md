# Repository Moved
This project has been moved to a new organization! https://github.com/Yuyu-billing

See our new home at:
- https://yuyu-billing.dev/
- https://github.com/Yuyu-billing/yuyu
- https://github.com/Yuyu-billing/yuyu_dashboard


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

```python
YUYU_URL="http://yuyu_server_url:8182"
CURRENCIES = ('IDR',)
DEFAULT_CURRENCY = "IDR"
```

Then restart Horizon.

## Multi Region

If your openstack using multiple region, and each region have its own Yuyu server, you can specify Yuyu server URL for each region.

To do that, you can add `YUYU_URL_REGION` to horizon `local_settings.py`

`YUYU_URL_REGION` is a list of tuples which define a mapping from region name (as in horizon `AVAILABLE_REGIONS`) to Yuyu URL for each. The tuple format is ***('{{ region_name }}', 'http://{yuyu_url}')***.

For example:

```python
# Example AVAILABLE_REGIONS settings

AVAILABLE_REGIONS = [
    ("https://172.12.12.10:5000/v3", 'US'),
    ("https://172.12.12.11:5000/v3", 'Singapore')
]

# Set Yuyu URL for each region
YUYU_URL_REGION = [
    ('US', 'http://region_a_yuyu_server_url:8182'),
    ('Singapore', 'http://region_b_yuyu_server_url:8182'),
]
```
