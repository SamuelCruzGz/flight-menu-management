# Architecture Decisions

This document records the main architectural decisions taken during the design phase of the project.

Its purpose is to explain **why** specific design choices were made, complementing the source code, which explains **how** they were implemented.

## Flight

### Decision

Flight represents a flight route, not a flight execution.

### Reason

The provided model does not include a departure date. Therefore, Flight is modeled as a reusable route that can have multiple menus over time.

---

## Menu

### Cycle

#### Decision

Cycle represents the menu rotation cycle.

#### Reason

Using Breakfast/Lunch/Dinner would duplicate the responsibility already handled by `Dish.meal_code`.

### Status

#### Decision

Menu status is managed by the application and is never provided by API consumers.

#### Reason

The application determines the correct status based on business rules, preventing inconsistent states from being introduced by client requests.
The calculated status is exposed in API responses and can be used as a search filter.

---

## Dish

### Ownership

#### Decision

A Dish belongs to a Menu and is created as part of the menu creation process.

#### Reason

The proposed data model defines a direct relationship through `menu_id` and does not include a reusable dish catalog.

As a consequence:

- Dishes do not exist independently.
- `POST /menus` creates both the Menu and its Dishes within the same transaction.
- Standalone CRUD endpoints for Dish are intentionally omitted.

### Name Validation

#### Decision

Dish names are normalized only during validation.

#### Reason

Formatting differences such as uppercase letters, extra spaces or underscores should not create duplicate dishes within the same menu.

The normalized value is used only during validation and is never persisted in the database.

## Soft Delete

### Decision

Menus are logically deleted using the `deleted_at` column instead of performing a physical deletion.

### Reason

The technical assessment explicitly requires soft deletion.

This approach preserves historical information, enables auditing, and prevents accidental data loss.

Active menus are identified by `deleted_at IS NULL`.

## Database Constraints

### Decision

Business rules such as preventing duplicated menus for the same flight and date range are enforced at the database level using `UniqueConstraint`.

### Reason

The Service layer performs friendly validation, while the database guarantees data integrity regardless of the application layer.

## API Schemas

### Decision

Database models and API schemas are intentionally separated.

### Reason

SQLAlchemy models represent persistence.

Pydantic schemas represent the API contract.

Keeping both layers independent allows different request and response contracts without coupling them to the database structure.

## Flight Identifier

### Decision

The API uses `flight_number` instead of the internal `flight_id` in request payloads whenever the client needs to identify a flight.

### Reason

`flight_number` is a business identifier known by API consumers, while `flight_id` is an internal database identifier.

Keeping `flight_id` internal reduces coupling between clients and the persistence layer, resulting in a more stable API contract.

The service layer is responsible for resolving the corresponding `flight_id` before interacting with the repository.

## Input Normalization

### Decision

User input is normalized in the service layer before being persisted.
Normalization is considered a technical concern and is isolated from the business domain.

### Reason

API consumers may provide equivalent values using different languages or formats (e.g. `week_1`, `Week_1`, `semana_1`).

The service layer converts those values into a single canonical representation before interacting with the repository, while the database stores only normalized values.

## Validation Strategy

### Decision

Request consistency is validated in the Service layer whenever it can be determined without accessing the database.

Database constraints are reserved for enforcing persistence integrity.

### Reason

Avoiding unnecessary database queries improves performance while keeping the database as the final authority for data integrity.


## Transaction Management

### Decision

Repositories never commit or rollback transactions.

Transaction boundaries are managed by the Service layer.

### Reason

A single business operation may involve multiple repositories.

Managing the transaction in the Service layer guarantees that all persistence operations succeed or fail as a single unit of work.

## Repository Filters

### Decision

Repositories receive dedicated filter objects instead of API schemas or long parameter lists.

### Reason

Filter objects keep repositories independent from the API layer while providing a scalable way to extend search criteria without continuously changing repository method signatures.

This approach keeps responsibilities separated:

- Pydantic schemas validate API requests.
- Filter objects transport search criteria between layers.
- Repositories remain focused on persistence concerns.

## Dependency Injection

### Decision

Services are instantiated through FastAPI dependency injection.

### Reason

Repositories and database sessions are created outside the business layer, allowing Services to remain independent from the web framework while keeping dependency construction centralized.