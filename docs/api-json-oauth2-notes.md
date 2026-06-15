# API, JSON and OAuth2 Notes

These notes summarize basic concepts used in many Python Data/BI workflows.

---

## API Basics

An API allows software systems to exchange data through defined endpoints.

A typical API workflow is:

1. send a request to an endpoint
2. receive a response
3. parse the response body
4. extract relevant fields
5. transform the result into a useful structure
6. save or analyze the result

Many APIs return JSON.

---

## JSON Basics

JSON stands for JavaScript Object Notation.

In Python, JSON data usually becomes:

| JSON concept | Python equivalent |
|---|---|
| object | dictionary |
| array | list |
| string | string |
| number | int or float |
| true / false | True / False |
| null | None |

Nested JSON responses are common in API work. For Data/BI workflows, selected nested values often need to be transformed into a flat table.

---

## OAuth2 Basics

OAuth2 is an authorization framework.

It is often used when an application needs controlled access to a service on behalf of a user or system.

Important terms:

| Term | Meaning |
|---|---|
| Client ID | Public identifier for an application |
| Client Secret | Private secret for an application |
| Access Token | Short-lived token used to call protected APIs |
| Refresh Token | Token used to request a new access token |
| Scope | Permission level requested by the application |
| Redirect URI | URL where the authorization server sends the result |
| Authorization Server | System that issues tokens |
| Resource Server | API that accepts valid access tokens |

---

## Security Rules

Never commit real secrets to Git.

Do not commit:

- API keys
- access tokens
- refresh tokens
- client secrets
- private `.env` files
- downloaded credential files
- personal data
- customer data

Use `.env.example` files or placeholders instead.

---

## Why This Matters for Data/BI

API and OAuth2 basics matter because many real Data/BI systems need to connect to external platforms, internal tools or cloud services.

A safe workflow must separate:

- code
- configuration
- credentials
- data
- documentation

This repository keeps OAuth2 as concept notes for now. That is intentional.
