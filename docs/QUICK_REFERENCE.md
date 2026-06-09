# Quick Reference Guide

## 🚀 Getting Started (3 Steps)

### Step 1: View Project Structure
```powershell
python config/project_info.py
```

### Step 2: Run Demo
```powershell
python app/main.py
```

### Step 3: Run Tests
```powershell
python tests/run_all_tests.py
```

## 📖 Common Commands

### Run Specific Component Tests
```powershell
# Shopping Cart Tests
python tests/test_cart.py

# Session Management Tests
python tests/test_session.py

# Dynamic Pricing Tests
python tests/test_pricing.py

# Recommendation Engine Tests
python tests/test_recommendation.py

# Knapsack Algorithm Tests
python tests/test_knapsack.py

# Integration Tests
python tests/test_integration.py
```

### Interactive Menus
```powershell
# Helper menu (recommended)
python run.py

# Quick test selector
python tests/quick_test.py
```

## 💻 Code Examples

### Example 1: Basic Setup
```python
from src.engines.ecommerce_engine import ECommerceEngine

engine = ECommerceEngine()
```

### Example 2: Create User & Add to Cart
```python
# Create user
engine.create_user(1, "premium")

# Setup product
engine.pricing_engine.set_base_price(101, 1000)
engine.pricing_engine.update_inventory(101, 50)

# Add to cart
engine.add_to_cart(1, 101, quantity=2)

# Get cart summary
cart = engine.get_cart_summary(1)
print(f"Total: Rs. {cart['total']:.2f}")
```

### Example 3: Get Recommendations
```python
# Track user behavior
engine.track_view(1, 101)
engine.track_view(1, 102)
engine.track_purchase(1, 101)

# Get recommendations
recommendations = engine.get_recommendations(1, k=5)
for product_id, score in recommendations:
    print(f"Product {product_id}: Score {score:.4f}")
```

### Example 4: Dynamic Pricing
```python
# Add pricing rules
engine.pricing_engine.add_pricing_rule(
    min_inv=0, 
    max_inv=10, 
    multiplier=1.15,  # +15% for low stock
    priority=1,
    rule_name="Low Stock Premium"
)

# Get price
price = engine.get_price(101, 1)
breakdown = engine.get_price_breakdown(101, 1)
```

### Example 5: Bundle Optimization
```python
# Add deals
engine.deal_selector.add_deal(101, 1000, 10)  # 10% off
engine.deal_selector.add_deal(102, 500, 15)   # 15% off

# Optimize bundle
bundle = engine.optimize_bundle(1, max_budget=2000)
print(f"Bundle: {bundle['bundle']}")
print(f"Total: Rs. {bundle['total_value']:.2f}")
```

## 🧪 Testing Individual Components

### Test Shopping Cart
```python
from src.models.cart import ShoppingCart

cart = ShoppingCart(user_id=1)
cart.add_item(101, 2, 500.0)
cart.add_item(102, 1, 300.0)

print(f"Total: Rs. {cart.get_total():.2f}")
print(f"Items: {cart.size}")
```

### Test User Session
```python
from src.models.session import UserSession

session = UserSession(1, "premium")
session.add_view(101)
session.add_view(102)
session.add_purchase(101)

recent = session.get_recent_browsing(5)
summary = session.get_summary()
```

### Test Recommendation Graph
```python
from src.engines.recommendation import RecommendationGraph

graph = RecommendationGraph()
graph.add_interaction(1, 101, weight=2.0)
graph.add_interaction(1, 102, weight=1.0)

recommendations = graph.personalized_pagerank(1, top_k=5)
```

### Test Dynamic Pricing
```python
from src.engines.pricing import DynamicPricingEngine

pricing = DynamicPricingEngine()
pricing.set_base_price(101, 1000)
pricing.update_inventory(101, 5)
pricing.add_pricing_rule(0, 10, 1.15, priority=1)
pricing.set_user_segment(1, "premium")

price = pricing.calculate_price(101, 1)
```

### Test Knapsack
```python
from src.utils.knapsack import bundle_optimization

products = [
    (101, 100),
    (102, 200),
    (103, 300)
]

bundle = bundle_optimization(products, max_budget=400)
print(f"Selected products: {bundle}")
```

## 📊 Component Reference

| Component | File | Key Methods |
|-----------|------|-------------|
| Shopping Cart | `src/models/cart.py` | `add_item()`, `remove_item()`, `get_total()` |
| User Session | `src/models/session.py` | `add_view()`, `add_purchase()`, `get_summary()` |
| Pricing Engine | `src/engines/pricing.py` | `calculate_price()`, `add_pricing_rule()` |
| Recommendations | `src/engines/recommendation.py` | `personalized_pagerank()`, `add_interaction()` |
| Deal Selector | `src/engines/deal_selector.py` | `add_deal()`, `get_top_deals()` |
| Knapsack | `src/utils/knapsack.py` | `bundle_optimization()` |
| Main Engine | `src/engines/ecommerce_engine.py` | All integrated methods |

## 🔑 Key Configuration

Edit `config/settings.py` to customize:
- PageRank damping factor (default: 0.85)
- Number of iterations (default: 20)
- Session timeout (default: 1800s)
- Top deals count (default: 5)

## 📁 File Structure Quick Reference

```
src/
├── models/          # Data models (Cart, Session, Pricing Rule)
├── engines/         # Core engines (Recommendation, Pricing, Deals, Main)
└── utils/          # Utilities (Knapsack algorithms)

app/
└── main.py         # Demo application

tests/
├── test_*.py       # Individual test suites
├── run_all_tests.py    # Run all tests
└── quick_test.py       # Interactive test menu

config/
├── settings.py         # Configuration
└── project_info.py     # Structure visualizer
```

## ⚡ Performance Tips

1. **PageRank Iterations**: Reduce for faster recommendations (default: 20)
2. **Knapsack Budget**: Use integers for better performance
3. **Heap Size**: Adjust top-k deals count based on needs

## 🐛 Troubleshooting

### Import Errors
Make sure you're running from the project root:
```powershell
cd "e:\DSA EL"
python app/main.py
```

### Test Failures
Run individual test files to isolate issues:
```powershell
python tests/test_cart.py -v
```

### Module Not Found
Ensure Python path is set correctly. Tests use `sys.path.insert()` automatically.

## 📚 Further Reading

- `README.md`: Complete documentation
- `PROJECT_SUMMARY.md`: Comprehensive project overview
- Source files: Detailed docstrings in each file

## 🎯 Quick Workflow

1. **View structure**: `python config/project_info.py`
2. **Run demo**: `python app/main.py`
3. **Run tests**: `python tests/run_all_tests.py`
4. **Explore code**: Start with `src/engines/ecommerce_engine.py`
5. **Customize**: Edit `config/settings.py`

## ✅ Verification Checklist

- [ ] Project structure visible: `python config/project_info.py`
- [ ] Demo runs successfully: `python app/main.py`
- [ ] All tests pass: `python tests/run_all_tests.py`
- [ ] Individual components work
- [ ] Documentation reviewed

---

**Need help?** Check `README.md` or `PROJECT_SUMMARY.md` for detailed information.
