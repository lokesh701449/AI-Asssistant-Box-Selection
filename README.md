# AI-Assisted Box Selection System

A production-quality Django REST Framework (DRF) project built for recommending the best/cheapest shipping boxes for orders. Designed as a Python Developer Internship assignment.

---

## Technical Stack
- **Backend:** Python 3.11+, Django 5.0+, Django REST Framework 3.17+
- **Database:** SQLite (Default, preconfigured)
- **Testing:** pytest, pytest-django

---

## Architectural Choices & Code Structure
The system is built with a clean separation of concerns:
- **Models (`core/models.py`):** Holds the database schema. Utilizes Django validators (e.g. `MinValueValidator`) to guarantee data integrity at the database layer. Calculates read-only helper properties like `volume` and `sorted_dimensions`.
- **Service Layer (`core/services.py`):** Houses the box recommendation algorithm, separating critical business rules from views and serializers. This makes the logic highly testable and decoupled from the HTTP transport layer.
- **Serializers (`core/serializers.py`):** Customizes the presentation layer, validates incoming payloads, and handles **writable nested structures** (e.g., creating/updating orders along with their items in a single atomic transaction).
- **ViewSets (`core/views.py`):** Clean REST viewsets mapping Standard REST actions (CRUD) to DRF Router-defined paths. Features a custom API action `recommend-box` to run the recommendation service.

---

## Recommendation Engine Logic
To find the cheapest box that fits all products in an order while avoiding NP-Hard 3D bin packing overengineering, the recommendation engine evaluates all candidate boxes against the following criteria:

1. **Total Weight Constraint:** The total weight of all items in the order ($\sum \text{weight} \times \text{quantity}$) must be $\le$ the box's `max_weight`.
2. **Individual Fit Constraint:** Each product in the order must physically fit inside the box's dimensions. To support rotation (e.g., turning a flat item to fit), both product dimensions and box dimensions are sorted prior to comparison (shortest-to-shortest, medium-to-medium, longest-to-longest).
3. **Total Volume Constraint:** The sum of the volumes of all items must be $\le$ the box's inner volume ($\text{length} \times \text{width} \times \text{height}$).

### Optimization & Tie-Breaking:
- Candidate boxes are filtered to only those that meet the criteria above.
- Candidates are then sorted by **cost** (ascending).
- If multiple boxes have the identical minimum cost, the tie is broken by choosing the box with the **smallest inner volume** (ascending).

---

## Setup & Running the Project Locally

### 1. Prerequisites
- Python 3.11+
- `pip`

### 2. Install & Activate Virtual Environment
```bash
# Clone or navigate to the directory
cd "AI-Assisted Box Selection System"

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the Application
To run the local development server:
```bash
python manage.py runserver
```
The API root will be accessible at: `http://127.0.0.1:8000/api/`

---

## Running Automated Tests
Tests are located in `core/tests/` and cover models, services, and viewsets. Run them with:
```bash
pytest
```

---

## API Documentation & Sample Requests

### 1. Products API (`/api/products/`)

#### List all products
- **Method:** `GET`
- **Request:**
  ```bash
  curl -X GET http://127.0.0.1:8000/api/products/
  ```

#### Create a product
- **Method:** `POST`
- **Request:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/products/ \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Smartphone",
      "length": 15.50,
      "width": 8.00,
      "height": 1.20,
      "weight": 0.20
    }'
  ```

---

### 2. Boxes API (`/api/boxes/`)

#### List all boxes
- **Method:** `GET`
- **Request:**
  ```bash
  curl -X GET http://127.0.0.1:8000/api/boxes/
  ```

#### Create a box
- **Method:** `POST`
- **Request:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/boxes/ \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Standard Small Box",
      "inner_length": 20.00,
      "inner_width": 15.00,
      "inner_height": 10.00,
      "max_weight": 5.00,
      "cost": 1.50
    }'
  ```

---

### 3. Orders API (`/api/orders/`)

#### Create a new order with items (Writable Nested Serializer)
- **Method:** `POST`
- **Request:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/orders/ \
    -H "Content-Type: application/json" \
    -d '{
      "items": [
        {
          "product": 1,
          "quantity": 2
        }
      ]
    }'
  ```

---

### 4. Recommendation Endpoint (`/api/orders/<id>/recommend-box/`)

#### Recommend box for Order #1
- **Method:** `GET`
- **Request:**
  ```bash
  curl -X GET http://127.0.0.1:8000/api/orders/1/recommend-box/
  ```
- **Sample Success Response:**
  ```json
  {
    "message": "Best box recommended successfully.",
    "recommended_box": {
      "id": 1,
      "name": "Standard Small Box",
      "inner_length": "20.00",
      "inner_width": "15.00",
      "inner_height": "10.00",
      "max_weight": "5.00",
      "cost": "1.50",
      "volume": "3000.00"
    }
  }
  ```
