# Architecture Decisions

This document records the main architectural decisions taken during the design phase of the project.

Its purpose is to explain **why** specific design choices were made, complementing the source code, which explains **how** they were implemented.

## Flight

### Decision

Flight represents a flight route, not a flight execution.

### Rationale

The provided model does not include a departure date. Therefore, Flight is modeled as a reusable route that can have multiple menus over time.

---

## Menu

### Cycle

#### Decision

Cycle represents the menu rotation cycle.

#### Rationale

Using Breakfast/Lunch/Dinner would duplicate the responsibility already handled by `Dish.meal_code`.

### Status

#### Decision

Status represents the administrative state of the menu (`ACTIVE` / `INACTIVE`).

#### Rationale

Temporal states such as `FINISHED` can be derived from `start_date` and `end_date`, therefore they should not be persisted.

---

## Dish

### Ownership

#### Decision

A Dish belongs to a Menu and is created as part of the menu creation process.

#### Rationale

The proposed data model defines a direct relationship through `menu_id` and does not include a reusable dish catalog.

As a consequence:

- Dishes do not exist independently.
- `POST /menus` creates both the Menu and its Dishes within the same transaction.
- Standalone CRUD endpoints for Dish are intentionally omitted.

### Name Validation

#### Decision

Dish names are normalized only during validation.

#### Rationale

Formatting differences such as uppercase letters, extra spaces or underscores should not create duplicate dishes within the same menu.

The normalized value is used only during validation and is never persisted in the database.