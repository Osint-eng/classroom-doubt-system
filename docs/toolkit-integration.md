# Toolkit integration plan

Branch: `feat/toolkit-integration`

## What is integrated in this branch

### Postman
- Added `postman/Classroom-Doubt-System.postman_collection.json`.
- Covers API health, registration/login, question creation/listing, answer creation/listing.
- Uses a disposable `example.test` email and local base URL by default.
- Import the collection into Postman, set `baseUrl`, and run it against a disposable local/test database.
- This is a smoke-test collection, not a security test suite.

### Environment-based MongoDB configuration
- The FastAPI MongoDB client now reads `MONGO_URL` or `MONGO_URI` from the environment.
- No fallback credential is embedded in source.
- Set the new rotated URI in local `.env` (ignored by Git) and the hosting provider's secret environment settings.

## Recommended next tool integrations

| Tool | Fit | Why / next action |
|---|---|---|
| AG Grid | High for teacher/admin analytics | Frontend is represented as a Git submodule in this repo; need its source repo/access before adding a dashboard grid. |
| Postman | Implemented starter | Expand smoke tests into auth, validation, voting, duplicate requests, and error cases after API behavior is stabilized. |
| Render | Existing deployment config needs review | Current `render.yaml` targets a Flask app under `backend/`, while root `main.py` is FastAPI. Confirm intended production entry point before changing deployment. |
| Elastic | Optional | Consider only if question search needs full-text/hybrid search at scale; MongoDB queries may be enough initially. |
| Zapier | Optional | Add teacher notifications only after backend event handling and authorization are reliable. |
| APIMatic | Low/optional | Useful if the API contract is formalized (OpenAPI) and SDKs/docs are needed. |
| Astropods | Optional AI workflow | Consider for a bounded AI tutor/triage agent after defining trusted knowledge sources and teacher oversight. |
| Channel3 | Not a natural fit | Product discovery is unrelated to the core doubt workflow unless the app later adds learning-resource shopping/catalog discovery. |
| Bryntum | Low | Only needed if adding timetable, office-hours, or teacher booking calendars. |
| KERNEL | Low/optional | Browser automation is not required for the current core app; direct APIs are safer. |

## Current repo risks observed
- The repository contains both root FastAPI routes and a separate Flask backend directory; deployment config currently points to the Flask app.
- The frontend path is a submodule, so frontend component integration cannot be safely committed from this repository alone.
- Root FastAPI question/answer/voting endpoints currently do not consistently enforce authentication/authorization. Treat the Postman collection as smoke testing only and address access control before production.
- A MongoDB URI was committed in source. Rotating the credential is necessary; removing it from the latest file does not erase it from Git history.

## Validation status
- Postman collection JSON is generated from the observed route paths and request shapes.
- No API runtime tests were executed because the repository could not be cloned into the execution environment and no database credentials were configured.
- No deployment or external service action was performed.
