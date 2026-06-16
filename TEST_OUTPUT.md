# Test Output

## Automated Test Execution (`pytest`)

Below is the execution log of the full test suite comprising 16 unit and integration test cases:

```bash
============================= test session starts ==============================
platform darwin -- Python 3.11.8, pytest-9.1.0, pluggy-1.6.0
django: version: 5.0.14, settings: box_system.settings (from ini)
rootdir: /Users/chalasanilokesh/AI-Assisted Box Selection System
configfile: pytest.ini
plugins: django-4.12.0
collected 16 items

core/tests/test_models.py .....                                          [ 31%]
core/tests/test_services.py .......                                      [ 75%]
core/tests/test_views.py ....                                            [100%]

============================== 16 passed in 0.18s ==============================
```

---

## Manual Verification (Scenario Scenarios Execution)

Below is the execution output of the seeding and recommendation scenario verification script:

```bash
--- Seeding Database ---
Created Products: Smartphone (15.5x8.0x1.2 cm, 0.2 kg), Laptop (35.0x25.0x2.0 cm, 2.2 kg), Book (22.0x14.5x3.0 cm, 0.8 kg), Desk Lamp (45.0x20.0x20.0 cm, 1.5 kg)
Created Boxes: Letter Mailer (Cost: 0.5, Max Wt: 1.0 kg), Standard Box S (Cost: 1.2, Max Wt: 5.0 kg), Standard Box M (Cost: 2.2, Max Wt: 10.0 kg), Standard Box L (Cost: 3.5, Max Wt: 20.0 kg), Oversized Box (Cost: 7.0, Max Wt: 40.0 kg)

--- Running Test Recommendation Scenarios ---
Order 1 (1x Smartphone): Recommended Box -> Letter Mailer (Cost: 0.50, Max Wt: 1.00 kg)
Order 2 (1x Book): Recommended Box -> Standard Box M (Cost: 2.20, Max Wt: 10.00 kg)
Order 3 (1x Laptop): Recommended Box -> Standard Box L (Cost: 3.50, Max Wt: 20.00 kg)
Order 4 (1x Smartphone + 1x Laptop): Recommended Box -> Standard Box L (Cost: 3.50, Max Wt: 20.00 kg)
Order 5 (1x Desk Lamp): Recommended Box -> Oversized Box (Cost: 7.00, Max Wt: 40.00 kg)

--- All Scenarios Verified Successfully ---
```