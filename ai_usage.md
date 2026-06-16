# AI_USAGE.md

## AI Tools Used

The following AI tools were used during development:

* ChatGPT
* Antigravity AI Assistant

These tools were primarily used for:

* Project architecture brainstorming
* Django REST Framework structure generation
* Recommendation engine refinement
* Test generation
* Documentation drafting
* Mermaid diagram generation

---

# Prompts Used

## Prompt 1 — Initial Project Setup

```text
Create a production-style Django REST Framework project for a Python Developer Internship assignment.

Requirements:

Build an AI-assisted Box Selection System.

Tech Stack:
- Django
- Django REST Framework
- SQLite
- Pytest or Django test framework

Models Required:
1. Product
- name
- length
- width
- height
- weight

2. Box
- name
- inner_length
- inner_width
- inner_height
- max_weight
- cost

3. Order
- created_at

4. OrderItem
- order
- product
- quantity

Requirements:
- Create REST APIs for Products, Boxes, Orders
- Add endpoint to recommend best box for an order
- Recommendation rules:
  - All products must fit inside the box dimensions
  - Total order weight must be within box max_weight
  - Return cheapest fitting box
  - If multiple boxes same cost, return smallest volume box

Architecture Requirements:
- Use service layer for recommendation logic
- Keep serializers and views clean
- Use DRF ViewSets
- Add validations
- Use proper project structure
- Follow PEP8

Also generate:
- requirements.txt
- README.md structure
- sample API requests
- test structure

Do NOT overengineer.
Keep it internship-level but production-quality.
```

---

## Prompt 2 — Recommendation Engine

```text
Now implement the recommendation engine.

Create:
services/box_selector.py

Logic:
1. Calculate total order weight
2. Determine dimensions needed for all products
3. Check whether products fit in a box
4. Filter boxes by:
   - dimensions
   - max_weight
5. Return:
   - cheapest valid box
   - if tie: smallest volume

Implementation Notes:
- Sort product dimensions before comparison
- Sort box dimensions before comparison
- Use clean helper methods
- Add docstrings
- Keep code readable and maintainable

Also add edge case handling:
- no valid box
- empty order
- invalid quantities
```

---

## Prompt 3 — API Endpoints

```text
Add REST API endpoints using Django REST Framework.

Required endpoints:

/api/products/
/api/boxes/
/api/orders/
/api/orders/{id}/recommend-box/

Requirements:
- Use ViewSets + routers
- Return JSON responses
- Add serializer validations
- Use proper HTTP status codes

recommend-box response example:
{
  "recommended_box": "Medium Box",
  "cost": 120,
  "reason": "Cheapest box that fits dimensions and weight"
}

Also generate sample POST payloads.
```

---

## Prompt 4 — Test Cases

```text
Generate comprehensive Django test cases.

Test:
1. Product creation
2. Box creation
3. Order creation
4. Recommendation endpoint
5. Cheapest box selection
6. Weight overflow rejection
7. No valid box case
8. Tie-breaker by volume
9. Empty order validation

Use APITestCase or pytest.

Keep tests realistic and readable.
```

---

## Prompt 5 — README Generation

```text
Generate a professional README.md for the Django Box Recommendation System.

Include:
- Project overview
- Features
- Tech stack
- Setup instructions
- API endpoints
- Example requests/responses
- Running tests
- Design decisions
- Future improvements

Keep concise and professional.
```

---

## Prompt 6 — AI Usage Documentation

```text
Generate AI_USAGE.md for this assignment.

Include:
1. AI tools used
- ChatGPT
- Antigravity

2. How AI was used
- architecture brainstorming
- serializer structure
- test generation
- README drafting

3. What outputs were accepted
4. What outputs were modified manually
5. Mistakes AI made
- overengineered models
- incorrect box fitting assumptions
- missing validations
- inefficient queries

6. Verification steps
- manual API testing
- running test suite
- validating recommendation logic

Tone:
Honest, professional, reflective.
```

---

# Outputs Accepted

The following AI-generated outputs were accepted with minor adjustments:

* Initial Django project structure
* DRF ViewSet boilerplate
* Serializer structure
* Test scaffolding
* README draft
* Recommendation service helper methods
* Mermaid architecture diagrams

---

# Outputs Modified Manually

Several generated outputs were reviewed and improved manually:

* Simplified overly complex recommendation logic
* Refactored service structure for readability
* Added validation improvements
* Adjusted serializer behavior for nested order items
* Improved naming consistency
* Added helper properties for volume and dimension sorting
* Enhanced test coverage
* Refined documentation wording

---

# Mistakes Identified in AI Suggestions

During development, several AI-generated suggestions required correction:

1. Overengineered abstraction layers for a small assignment
2. Incorrect assumptions around product fitting logic
3. Missing edge-case handling for empty orders
4. Incomplete serializer validation
5. Inefficient recommendation filtering approaches
6. Poor naming conventions in early generated code
7. Lack of separation between API logic and business logic

These issues were manually corrected after verification and testing.

---

# Verification Process

The final implementation was verified using:

## Automated Testing

* Pytest-based unit and integration tests
* API endpoint validation tests
* Service layer recommendation tests

## Manual Validation

* Manual API testing using Postman
* Realistic order recommendation scenarios
* Validation of edge cases
* Verification of tie-break behavior

## Code Review

* Manual review for readability and maintainability
* Validation of recommendation correctness
* PEP8 compliance checks

---

# Final Notes

AI tools were used as development assistants rather than code generators alone. All generated outputs were reviewed, validated, modified where necessary, and tested manually before final submission.

The final implementation reflects both AI-assisted acceleration and manual engineering decisions.
