# py-switchbot-api
An asynchronous library to use Switchbot API. Allows to use both devices and remotes.

## Usage

```python
token = "xxx"
secret = "yyy"

client = SwitchBotAPI(token, secret)
print(await client.list_devices())
print(await client.get_status('some-id'))
await client.send_command('some-id', {COMMAND})
```

## Development

### Install

```bash
poetry install
```

### Lint

```bash
poetry run black switchbot_api/
poetry run mypy switchbot_api/
```
