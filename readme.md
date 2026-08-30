# PIChatBot

Create Virtual Environment 
```bash
python -m venv .venv
```

Activate Virtaul Environment
```bash
source .venv/Scripts/activate.bat
.\.venv\Scripts\activate.bat
activate
```

Deactivate Virtual Environment
```bash
source .venv/Scripts/deactivate
.\.venv\Scripts\deactivate.bat
deactivate
```

Install Dependenties (pyproject.toml)
```bash
python -m pip install -e .
```

pytest tests/e2e/test_websocket.py

```powershell
Remove-Item -Recurse -Force .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

get users
```bash
curl -k "http://192.168.1.27:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=user_list&version=2&token=AJ8PmR7K8u5NhfIV2BnO3ve0sdK2ey0V8nSe7yTjtR1gr9Y9SLQCmsILxWZlA0ek"
```

curl -X POST \
  "http://192.168.1.27:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=chatbot&version=2&token=AJ8PmR7K8u5NhfIV2BnO3ve0sdK2ey0V8nSe7yTjtR1gr9Y9SLQCmsILxWZlA0ek" \
  --data-urlencode 'payload={"text":"Hello from curl!","user_ids":[22]}'
