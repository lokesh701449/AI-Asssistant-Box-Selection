# System Design Notes

## Recommendation Logic Design

The recommendation engine was intentionally separated into a dedicated service layer to maintain clean separation of concerns between API views and business logic.

Core design principles followed:

* Thin views and serializers
* Centralized recommendation logic
* Extensible architecture for future shipping strategies
* Deterministic and testable outputs

---

## Recommendation Workflow

### Step 1: Validate Order

The engine first validates:

* Order contains at least one item
* Quantities are positive
* Products exist

### Step 2: Calculate Aggregate Constraints

The service computes:

* Total order weight
* Total required volume
* Maximum dimension requirements

### Step 3: Filter Candidate Boxes

Boxes are filtered using:

* Maximum supported weight
* Internal dimension compatibility
* Product orientation flexibility

Dimensions are sorted before comparison to allow rotational fitting.

Example:

Product:
(10, 20, 30)

Box:
(30, 10, 20)

Both become:
(10, 20, 30)

This allows realistic fitting behavior.

### Step 4: Ranking Strategy

Among valid boxes:

1. Lowest cost is prioritized
2. Smallest box volume is used as tie-breaker

This simulates cost-efficient packaging decisions in ecommerce systems.

---

# Architectural Decisions

## Why Service Layer?

Separating recommendation logic from views:

* Improves maintainability
* Simplifies testing
* Keeps APIs lightweight
* Enables future reuse

## Why DRF ViewSets?

ViewSets reduce boilerplate and provide scalable REST routing.

## Why Nested Order Items?

Nested order item creation simplifies API usage and better represents real ecommerce order structures.

## Why SQLite?

SQLite was selected for simplicity and assignment portability.

---

# Future Improvements

Potential production-scale improvements:

* Volumetric weight calculations
* Multiple box packing optimization
* AI/ML-based shipping prediction
* Warehouse availability constraints
* Fragile item handling
* Delivery priority optimization
* Rate-limited APIs
* Redis caching
* PostgreSQL migration
* Docker deployment
* Async processing with Celery

---

# Security & Validation

The system includes:

* Positive value validation
* Serializer-level validation
* Model constraints
* Controlled API exposure
* Error handling for invalid recommendations

---

# Performance Considerations

Current implementation is optimized for:

* Readability
* Correctness
* Small-to-medium order sizes

Future scaling optimizations may include:

* Precomputed box metadata
* Query optimization
* Cached recommendation responses
* Batch recommendation processing
