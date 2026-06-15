# Ollama Local API Notes

Ollama can expose a local HTTP API on a developer machine.

In this repository, Ollama is treated as an optional local API example, not as a production AI workflow.

---

## Local Endpoint

Default local endpoint:

```text
http://localhost:11434/api/generate
```

A Python script can send a JSON payload to this endpoint and receive a JSON response.

---

## Why This Fits Here

The learning value is not only the language model itself.

For Python/API basics, Ollama is useful because it demonstrates:

- sending JSON to an HTTP endpoint
- receiving JSON from an HTTP endpoint
- parsing response fields
- handling connection errors
- working with a local service instead of a cloud API

---

## Requirements

The example only works if:

- Ollama is installed
- Ollama is running locally
- the configured model is available

If these requirements are not met, the example should fail gracefully.

---

## Security Notes

The local Ollama example does not require:

- cloud API keys
- OAuth2 tokens
- client secrets
- external credentials

Do not add private prompts, personal data or sensitive documents to this repository.
