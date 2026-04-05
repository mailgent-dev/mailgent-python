# Hivekey Python SDK

The official Python SDK for the [Hivekey API](https://hivekey.ai) -- identity infrastructure for AI agents.

[![PyPI version](https://img.shields.io/pypi/v/hivekey.svg)](https://pypi.org/project/hivekey/)
[![Python 3.9+](https://img.shields.io/pypi/pyversions/hivekey.svg)](https://pypi.org/project/hivekey/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install hivekey
```

## Quick start

```python
from hivekey import Hivekey

client = Hivekey(api_key="mgent-...")

me = client.identity.whoami()
print(me.email)

client.mail.send(
    to=["colleague@example.com"],
    subject="Hello from my agent",
    text="Sent via the Hivekey Python SDK.",
)
```

## Async usage

```python
from hivekey import AsyncHivekey

async with AsyncHivekey(api_key="mgent-...") as client:
    me = await client.identity.whoami()
    await client.mail.send(
        to=["colleague@example.com"],
        subject="Hello",
        text="Sent asynchronously.",
    )
```

## Authentication

Pass your API key directly, or set the `HIVEKEY_API_KEY` environment variable:

```python
# Explicit
client = Hivekey(api_key="mgent-...")

# From environment
import os
os.environ["HIVEKEY_API_KEY"] = "mgent-..."
client = Hivekey()
```

Both `Hivekey` and `AsyncHivekey` support context managers for automatic resource cleanup:

```python
with Hivekey() as client:
    me = client.identity.whoami()
```

## Usage

### Identity

```python
me = client.identity.whoami()
print(me.email, me.display_name)
```

### Mail

```python
# Send
msg = client.mail.send(
    to=["alice@example.com"],
    subject="Weekly report",
    text="Plain text body",
    html="<h1>HTML body</h1>",
    cc=["bob@example.com"],
)

# Reply
client.mail.reply(message_id=msg.id, text="Got it, thanks!")

# List and read
messages = client.mail.list_messages(limit=10, labels=["INBOX"])
msg = client.mail.get_message(message_id="msg_123")

# Labels
client.mail.update_labels("msg_123", add_labels=["IMPORTANT"], remove_labels=["UNREAD"])

# Threads
threads = client.mail.list_threads(limit=5)
thread = client.mail.get_thread(thread_id="thread_123")

# Delete
client.mail.delete_message("msg_123")
client.mail.delete_thread("thread_123")
```

### Vault

```python
# Store a credential
client.vault.store(
    name="openai-key",
    type="api_key",
    data={"api_key": "sk-..."},
    metadata={"service": "openai"},
)

# Retrieve
cred = client.vault.get("openai-key")
print(cred.data)

# List all
creds = client.vault.list()

# Generate a TOTP code
totp = client.vault.totp("github-2fa")
print(totp.code)

# Delete
client.vault.delete("openai-key")
```

### Activity Logs

```python
# List logs with filters
logs = client.logs.list(limit=20, category="mail", status="success")

# Aggregate stats
stats = client.logs.stats()
```

### DID (Decentralized Identifiers)

```python
doc = client.did.resolve(identity_id="id_123")
domain_doc = client.did.resolve_domain()
```

## Error handling

All API errors raise `HivekeyError` with structured fields:

```python
from hivekey import HivekeyError

try:
    client.mail.send(to=["a@b.com"], subject="Hi", text="Hello")
except HivekeyError as e:
    print(e.status)   # HTTP status code
    print(e.code)     # Error code string
    print(e.message)  # Human-readable message
```

## Types

The SDK returns typed dataclasses, not raw dictionaries. API responses are automatically converted from camelCase to snake_case.

| Type | Description |
|------|-------------|
| `IdentityResponse` | Agent identity details |
| `MessageResponse` | Email message |
| `ThreadResponse` | Thread summary |
| `ThreadDetailResponse` | Thread with messages |
| `CredentialMetadata` | Vault credential metadata |
| `CredentialWithData` | Credential with decrypted data |
| `ActivityLog` | Single activity log entry |
| `LogsStats` | Aggregated log statistics |
| `TotpResponse` | Generated TOTP code |
| `DidDocument` | DID document |

> **Note:** The `from` field in message responses is exposed as `from_addrs` since `from` is a reserved keyword in Python.

## Requirements

- Python 3.9+
- [`httpx`](https://www.python-httpx.org/) (installed automatically)

## Links

- [Documentation](https://docs.hivekey.ai)
- [Console](https://console.hivekey.ai)
- [Website](https://hivekey.ai)
- [PyPI](https://pypi.org/project/hivekey/)

## License

MIT
