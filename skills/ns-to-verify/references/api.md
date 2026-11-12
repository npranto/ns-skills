# Proving an API or server change

A criterion with no screen is proven by a real request and its real response. A screenshot of a terminal proves nothing.

## The requests

For each endpoint, server action, or handler the change touches, send real requests against the running app:

| Case | Expect |
|---|---|
| Happy path | the documented status and body shape |
| Invalid input | a 4xx with the project's error shape, and nothing written |
| Empty and oversized input | handled, not a 500 |
| Signed out | 401, or a redirect to sign in |
| Another user's resource | 403 or 404, and nothing changed |
| The same write twice | the second is a no-op or a clear conflict, never a duplicate |

Save each request and response under `logs/`, with secrets and tokens redacted. The result card shows the status and the one line that proves the case.

## Worked example

Ticket: "Only the owner can archive a note."

```
POST /api/notes/n_123/archive   as the owner          -> 200  {"archivedAt":"2026-10-08T14:32:00Z"}
POST /api/notes/n_123/archive   as another user       -> 403  {"error":"forbidden"}
POST /api/notes/n_123/archive   signed out            -> 401
POST /api/notes/does-not-exist/archive                -> 404
POST /api/notes/n_123/archive   as the owner, again   -> 200  same archivedAt, no second write
```

Then read the row back: `archived_at` is set once, and the other user's attempt left no trace.

## Kept tests

Each row that is a permission or a business rule becomes an integration test through the real route and the real database (`../ns-route/references/topic-kept-tests.md` "Kept tests"). The test asserts the status and the stored state.

## Contract

When a response shape, status code, or error shape changes:

- Name every consumer: the frontend, another service, a webhook receiver, a mobile client.
- Additive changes (a new optional field) need no version. A removed or renamed field, a changed type, or a changed status is breaking: flag it, and expect the risk to be at least high (`/ns-route` "Reversibility").
- Old clients against the new server, and new clients against the old server, both work during a rollout.

## Jobs, webhooks, and queues

Trigger the real event. Confirm the message arrives once with the right payload, that a retry is safe, and that a failure leaves a log line someone could find.

## A hot path

When the change is on a path that is called often or the ticket is about speed: a fixed number of requests against the base and the change, reporting p50 and p95. Run both alternately, more than once, and say what limits the number.
