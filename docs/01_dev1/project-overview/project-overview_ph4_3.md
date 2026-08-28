# BizSC Project Overview

## 1. Project

**Project Name:** BizSC

BizSC is a personal web application development project for learning and
building a maintainable business-management application step by step.

The project emphasizes:

-   understanding each implementation before moving forward
-   clear separation of responsibilities
-   readability and maintainability
-   type safety
-   incremental development
-   testing and verification at each milestone

------------------------------------------------------------------------

## 2. Development Environment

Primary development environment:

``` text
OS              Windows
Editor          Cursor
Version Control Git / GitHub / GitHub Desktop
Containers      Docker Desktop / Docker Compose
Database Tool   TablePlus
```

Main workspace:

``` text
D:\Development\apps\bizsc
```

Repository:

``` text
https://github.com/eswm223-oss/bizsc
```

When code inspection is required, check the latest repository rather
than assuming that the handover documents exactly match the current
code.

------------------------------------------------------------------------

## 3. Technology Stack

### Frontend

``` text
React
TypeScript
Vite
React Router
Axios
CSS
```

### Backend

``` text
Python 3.13
FastAPI
Uvicorn
SQLAlchemy 2.x
Pydantic v2
Alembic
Argon2
pytest
```

### Database

``` text
PostgreSQL 17
```

### Infrastructure

``` text
Docker
Docker Compose
```

------------------------------------------------------------------------

## 4. Docker Services

BizSC is developed with three primary Docker Compose services.

``` text
frontend
backend
db
```

Ports:

``` text
Frontend    http://localhost:5173
Backend     http://localhost:8000
Swagger UI http://localhost:8000/docs
PostgreSQL  localhost:5432
```

Frontend source is mounted into the container for development.

The PostgreSQL Docker service is named:

``` text
db
```

Backend database configuration therefore uses `db` as the database host
inside the Compose network.

------------------------------------------------------------------------

## 5. System Architecture

Overall request flow:

``` text
Browser
  ↓
React
  ↓
Frontend API Module
  ↓
Axios
  ↓
FastAPI Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

The frontend does not access PostgreSQL directly.

------------------------------------------------------------------------

## 6. Backend Design

Backend responsibilities are separated into:

``` text
Router
Service
Repository
Model
Schema
Database
```

### Router

Responsible for:

-   HTTP request/response
-   Path parameters
-   Query parameters
-   Request body
-   FastAPI dependencies
-   calling Service methods

### Service

Responsible for:

-   business logic
-   processing decisions
-   combining Repository operations
-   domain-level error handling

### Repository

Responsible for:

-   SQLAlchemy queries
-   database CRUD
-   filtering
-   sorting
-   pagination
-   counting query results

### Model

SQLAlchemy database models.

Current main domain model:

``` text
User
```

### Schema

Pydantic API input/output structures.

------------------------------------------------------------------------

## 7. Database Management

Database:

``` text
PostgreSQL 17
```

Schema changes are managed with Alembic.

Conceptually:

``` text
SQLAlchemy Model
      ↓
Alembic Migration
      ↓
PostgreSQL
```

The Phase4 list enhancements do not require database schema changes.

------------------------------------------------------------------------

## 8. User API

Implemented User CRUD endpoints:

``` text
POST   /users
GET    /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

Health endpoints have also been developed during earlier phases.

------------------------------------------------------------------------

## 9. GET /users

Phase4 extends the User list endpoint.

Current intended Query Parameters:

``` text
search
is_active
sort_by
sort_order
page
limit
```

Example:

``` text
GET /users
    ?search=test
    &is_active=true
    &sort_by=email
    &sort_order=asc
    &page=1
    &limit=10
```

------------------------------------------------------------------------

## 10. User Search

Phase4 Step5 added email search.

Search field:

``` text
User.email
```

Search behavior:

``` text
partial match
```

Conceptually:

``` python
User.email.like(f"%{search}%")
```

Status:

**Completed**

------------------------------------------------------------------------

## 11. Active Filter

Phase4 Step6 added filtering by User active state.

Query Parameter:

``` text
is_active
```

Frontend choices:

``` text
全て
有効
無効
```

Frontend conversion:

``` text
""      → undefined
"true"  → true
"false" → false
```

Status:

**Completed**

------------------------------------------------------------------------

## 12. Sorting

Phase4 Step7 added sorting.

Query Parameters:

``` text
sort_by
sort_order
```

Supported sort fields:

``` text
id
email
created_at
updated_at
```

Sort order:

``` text
asc
desc
```

The Repository maps allowed strings to SQLAlchemy columns rather than
directly inserting an arbitrary client-provided column name into the
query.

Default behavior:

``` text
sort_by    = id
sort_order = asc
```

Status:

**Completed**

------------------------------------------------------------------------

## 13. Pagination

Phase4 Step8 adds pagination using:

``` text
page
limit
```

Default values:

``` text
page  = 1
limit = 10
```

Offset calculation:

``` python
offset = (page - 1) * limit
```

Examples:

``` text
page=1, limit=10 → offset=0
page=2, limit=10 → offset=10
page=3, limit=10 → offset=20
```

Repository query order conceptually:

``` text
select(User)
↓
search
↓
is_active
↓
sort
↓
offset
↓
limit
```

Status:

**Implementation through Step8-12 completed. Browser final verification
remains.**

------------------------------------------------------------------------

## 14. Pagination Total Count

Pagination requires two different values:

``` text
users
total
```

`users` contains only the current page.

`total` represents the number of Users matching search/filter conditions
before pagination.

Therefore:

``` text
total != len(users)
```

in general.

A Repository `count_all()` operation was added for this purpose.

Conceptually:

``` text
search
+
is_active
↓
COUNT
↓
total
```

Sorting and pagination are not needed when calculating `total`.

------------------------------------------------------------------------

## 15. User List Response

The User list response contains:

``` text
users
total
```

Meaning after pagination implementation:

``` text
users
→ records displayed on the current page

total
→ total records after search/filter but before pagination
```

Frontend uses `total` to calculate the number of pages.

------------------------------------------------------------------------

## 16. Frontend Structure

Main frontend structure:

``` text
frontend/
└─ src/
   ├─ api/
   ├─ components/
   ├─ layouts/
   ├─ pages/
   ├─ routes/
   └─ types/
```

Main API modules include:

``` text
api/client.ts
api/health.ts
api/users.ts
```

Main User pages include:

``` text
UserListPage
UserDetailPage
UserCreatePage
UserEditPage
```

------------------------------------------------------------------------

## 17. Frontend Routing

Primary routes:

``` text
/
├─ /users
├─ /users/new
├─ /users/:userId
└─ /users/:userId/edit

*
└─ NotFoundPage
```

React Router is used for routing.

------------------------------------------------------------------------

## 18. Shared UI Components

Shared components developed during Phase3 include:

``` text
Button
Card
Input
Loading
ErrorMessage
Badge
UserForm
```

The project avoids moving business logic into generic UI components.

------------------------------------------------------------------------

## 19. Page / Component Responsibility

### Page

Responsible for:

``` text
State
API calls
React Router
submit processing
API error handling
Loading state
page-specific validation
page-specific behavior
```

### Component

Responsible for:

``` text
UI
layout
props-driven rendering
user event notification
```

Generic Components should not normally call application APIs directly.

------------------------------------------------------------------------

## 20. UserForm

`UserForm` is shared by User creation and editing.

It handles UI such as:

``` text
email input
password input
Active input
field error display
submit button
form layout
```

Page-level responsibilities remain outside UserForm:

``` text
API calls
Axios error handling
navigation
business logic
page-specific validation decisions
```

------------------------------------------------------------------------

## 21. UserListPage

The User list page currently combines:

``` text
User table
email search
Active filter
sorting
pagination
```

Main State conceptually includes:

``` text
users
isLoading
error

search
activeFilter

sortBy
sortOrder

page
limit
total
```

------------------------------------------------------------------------

## 22. Frontend getUsers()

The frontend User API module conceptually supports:

``` ts
getUsers(
  search?,
  isActive?,
  sortBy?,
  sortOrder?,
  page?,
  limit?,
)
```

Frontend-to-Backend parameter mapping:

``` text
search     → search
isActive   → is_active
sortBy     → sort_by
sortOrder  → sort_order
page       → page
limit      → limit
```

Frontend uses camelCase while Backend Query Parameters use snake_case
where appropriate.

------------------------------------------------------------------------

## 23. Pagination UI

UserListPage has pagination controls conceptually displayed as:

``` text
前へ   1 / 3   次へ
```

Page count:

``` tsx
const totalPages = Math.max(1, Math.ceil(total / limit));
```

Behavior:

``` text
first page
→ Previous disabled

last page
→ Next disabled
```

When the user performs a new search, the page returns to page 1.

When changing pages, current search/filter/sort conditions must remain
active.

------------------------------------------------------------------------

## 24. Initial Data Loading

UserListPage uses `useEffect` for initial User loading.

During Phase4, the React lint warning related to synchronously calling
State setters from the effect body was addressed by separating initial
asynchronous loading from user-triggered loading.

The initial request stores both:

``` text
users
total
```

Cleanup logic prevents State updates after unmount.

------------------------------------------------------------------------

## 25. Validation Policy

Validation exists on both frontend and backend.

``` text
Frontend
→ early feedback / UX

Backend
→ final data guarantee
```

Backend remains the final authority for validation.

------------------------------------------------------------------------

## 26. Error Handling

Field-specific errors are displayed near the related input.

Page/API failures use the common `ErrorMessage` component.

An empty search/filter result is not treated as an API error.

------------------------------------------------------------------------

## 27. Loading / Submission State

Main UI state patterns include:

``` text
isLoading
isSubmitting
isDeleting
```

Buttons are disabled when necessary to prevent duplicate actions.

List re-fetch operations such as search, filter, sort and page movement
also use the loading state.

------------------------------------------------------------------------

## 28. CSS Policy

Responsibility:

``` text
Component CSS
→ appearance of the reusable component itself

Page CSS
→ page-specific placement and layout
```

UserListPage-specific search/filter/sort/pagination layout belongs in:

``` text
UserListPage.css
```

------------------------------------------------------------------------

## 29. TypeScript Policy

The project prioritizes type safety.

Guidelines:

-   avoid unnecessary `any`
-   define API response types
-   safely narrow caught errors
-   explicitly type Component Props
-   handle optional values intentionally
-   use React event types compatible with the current React/TypeScript
    environment

Current form submit handlers use:

``` tsx
React.SubmitEvent<HTMLFormElement>
```

where applicable.

------------------------------------------------------------------------

## 30. Backend Query Responsibility

For the User list, the Repository is responsible for constructing the
database query.

Conceptual flow:

``` text
Router receives Query Parameters
↓
Service forwards/coordinates conditions
↓
Repository constructs SQLAlchemy query
↓
Database executes query
```

The Router should not contain SQL query logic.

------------------------------------------------------------------------

## 31. Development Progress

### Phase1 --- Environment

**Completed**

Main outcomes:

``` text
Docker environment
Frontend container
Backend container
PostgreSQL container
Git/GitHub workflow
```

### Phase2 --- Backend CRUD

**Completed**

Main outcomes:

``` text
User model
Schemas
Repository
Service
Router
CRUD API
Alembic
Validation
Error handling
Tests
```

### Phase3 --- Frontend CRUD / Shared UI

**Completed**

Main outcomes:

``` text
routing
User list
User detail
User create
User edit
User delete
shared UI components
UserForm
loading/error handling
```

### Phase4 --- User List Enhancements / Tests

**In progress**

``` text
Step5  User search                 Completed
Step6  Active filter               Completed
Step7  Sorting                     Completed
Step8  Pagination                  Step8-12 completed
Step9  CRUD / list API tests       Not started
Step10 Phase4 final verification   Not started
```

------------------------------------------------------------------------

## 32. Current Exact Position

Current working position:

> **Phase4 Step8-13 --- Browser final verification of pagination**

Step8 implementation completed through:

``` text
Step8-1  Repository page/limit parameters
Step8-2  offset/limit query
Step8-3  Service page/limit
Step8-4  Router page/limit
Step8-5  Repository count_all()
Step8-6  Service users/total
Step8-7  Router total response
Step8-8  Swagger verification
Step8-9  Frontend API page/limit
Step8-10 UserListPage pagination State
Step8-11 Previous/Next logic
Step8-12 Pagination UI
```

------------------------------------------------------------------------

## 33. Step8-13 Verification

Next browser checks:

``` text
1. Previous is disabled on page 1
2. Next moves to page 2
3. page 2 displays different records
4. Previous returns to page 1
5. Next is disabled on the last page
6. pagination works with search
7. pagination works with Active filter
8. pagination works with sorting
9. a new search returns to page 1
10. zero results do not cause an error
```

Most important combined behavior:

``` text
search
+
Active filter
+
sorting
+
pagination
```

must work together.

After successful verification:

``` text
Phase4 Step8 = Completed
```

------------------------------------------------------------------------

## 34. Next Phase4 Work

After Step8:

### Step9

CRUD / User list API test additions.

Likely areas:

``` text
CRUD
search
is_active
sorting
pagination
total
```

The exact test plan must be based on the latest repository code and
existing test structure.

### Step10

Phase4 final verification.

Expected checks include:

``` text
Swagger UI
Browser
Frontend build
pytest
Git status
documentation
```

------------------------------------------------------------------------

## 35. GitHub Verification Rule

Repository:

``` text
https://github.com/eswm223-oss/bizsc
```

When beginning a new chat, inspect the latest code before giving
code-specific instructions.

Important files for the current Phase4 work:

``` text
backend/app/repositories/user.py
backend/app/services/user.py
backend/app/api/users.py

frontend/src/api/users.ts
frontend/src/pages/UserListPage.tsx
frontend/src/pages/UserListPage.css
frontend/src/types/user.ts
```

If the handover documents and GitHub differ, do not guess which version
is correct.

Confirm whether local changes have been committed and pushed.

------------------------------------------------------------------------

## 36. Documentation

Project documentation is maintained under the BizSC documentation
workflow.

Main handover documents:

``` text
project-overview.md
architecture.md
handover_phase.md
```

Documents are regenerated at meaningful milestones rather than after
every small code change.

For this handover generation, the corresponding files are:

``` text
architecture_ph4_3.md
handover_phase4_3.md
project-overview_ph4_3.md
```

------------------------------------------------------------------------

## 37. Development Workflow

Preferred workflow:

``` text
Explain one small step
↓
User implements it
↓
User verifies it
↓
User reports "StepX complete"
↓
Proceed to the next step
```

Avoid large batches of changes.

Before proposing code modifications:

``` text
check current implementation
understand existing structure
make the smallest necessary change
verify behavior
```

Commit / Push reminders should be given at meaningful stopping points.

------------------------------------------------------------------------

## 38. Next Chat Start Procedure

Recommended next-chat procedure:

``` text
1. Read project-overview_ph4_3.md
2. Read architecture_ph4_3.md
3. Read handover_phase4_3.md
4. Inspect latest GitHub code
5. Confirm Step8 changes are pushed
6. Resolve any document/code difference
7. Resume Phase4 Step8-13
8. Complete Step8
9. Begin Step9 tests
```

**Resume point: Phase4 Step8-13.**
