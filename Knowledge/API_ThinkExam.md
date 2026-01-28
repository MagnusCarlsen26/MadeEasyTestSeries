# ThinkExam API Implementation

## Overview
The project interacts with the ThinkExam backend used by MadeEasy. The API uses a custom request structure where payloads are double-JSON-encoded and sent as form-data.

## Endpoint Behavior
- **URL**: `https://think.thinkexam.com/api/v1/`
- **Method**: `POST`
- **Payload Format**: A single form key `data` containing a JSON string.
- **Dynamic Session Handling**: The API returns a new `ACCESS_TOKEN` in the response body. This token **must** be used in the `accessToken` field of the next request's payload to maintain the session.

## Critical Headers
- `custom-header`: A JSON string containing a temporary login `token` and `loginTime`.
- `authorization`: A static/long-lived bearer-style token used for initial handshaking.
- `Referer`: Must be set to `https://ots2026.onlinetestseriesmadeeasy.in/` to avoid origin rejection.
