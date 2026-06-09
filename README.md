# DSA-Driven E-Commerce Personalization Engine

> A full-stack e-commerce recommendation system built entirely on classical Data Structures & Algorithms — **no Machine Learning, no neural networks, no black boxes.** Every recommendation is fully traceable and explainable.

**Academic Project · CS-B2 DSA Lab · RVCE**

---

## Screenshots

### Products Page
![Products Page](assets/Screenshot%202026-06-09%20162951.png)

### Landing Page
![Landing Page](assets/Screenshot%202026-06-09%20163000.png)

### Time Complexity
![Time Complexity](assets/Screenshot%202026-06-09%20163020.png)

### Data Structures Used
![Data Structures Used](assets/Screenshot%202026-06-09%20163030.png)

### Recommendation Engine
![Recommendation Engine](assets/Screenshot%202026-06-09%20163045.png)

### Working
![Working](assets/Screenshot%202026-06-09%20163102.png)

### Summary
![Summary](assets/Screenshot%202026-06-09%20164426.png)

---

## Table of Contents

1. [What This Project Is](#what-this-project-is)
2. [Core Philosophy](#core-philosophy)
3. [Project Structure](#project-structure)
4. [Tech Stack](#tech-stack)
5. [Data Structures Implemented](#data-structures-implemented)
6. [Algorithms Implemented](#algorithms-implemented)
7. [Recommendation Pipeline](#recommendation-pipeline)
8. [Dynamic Pricing Engine](#dynamic-pricing-engine)
9. [API Endpoints](#api-endpoints)
10. [How to Run](#how-to-run)
11. [Data](#data)
12. [Frontend Features](#frontend-features)
13. [CLI Demo (Python-only)](#cli-demo-python-only)
14. [Complexity Analysis](#complexity-analysis)
15. [Mathematical Formulations](#mathematical-formulations)
16. [Future Scope](#future-scope)
17. [Project Statistics](#project-statistics)

---

## What This Project Is

This is a complete, production-grade e-commerce platform that demonstrates how **classical DSA concepts** can power real-world intelligent systems. It consists of:

- A **Flask REST API** (`backend/`) with 8 custom data structure implementations powering all recommendation, pricing, and cart operations
- A **React SPA** (`frontend/`) with real-time DSA visualizations using D3.js
- A **standalone Python library** (`src/`) and CLI demo (`app/`) that can run independently of the web app
- **100+ test cases** (`tests/`) covering every component

The central claim of the project: **recommendations that compete with ML-based systems are achievable using only deterministic algorithms** — and the bonus is full explainability.

---

## Core Philosophy

**ABSOLUTELY NO:**
- Machine Learning, Neural Networks, or Embeddings
- Gradient Descent or Vector Databases
- scikit-learn, TensorFlow, PyTorch, or any AI library
- Non-deterministic or black-box models

**ONLY:**
- Classical Data Structures (Graph, BST, Heap, Trie, Stack, Queue, Linked List, HashMap)
- Deterministic Algorithms (PageRank, Jaccard Similarity, Knapsack DP, BFS/DFS)
- Rule-Based Systems (Dynamic Pricing)
- Set Operations (Collaborative Filtering)

Same input always produces the same output. Every recommendation comes with a "why" trace.

---

## Project Structure

```
DSA-ExpLearning/
│
├── README.md                    ← You are here (master documentation)
├── requirements.txt             ← Python dependencies (Flask, Flask-CORS only)
├── run.py                       ← Interactive CLI helper script
├── start.ps1                    ← PowerShell automated startup script
├── .gitignore
│
├── backend/                     ← Flask REST API (Python)
│   ├── app.py                   ← Flask server, all API endpoints (port 5000)
│   ├── models.py                ← Product, User, Transaction dataclasses
│   ├── sample_data.py           ← 89 products, 20 users, 100 transactions
│   ├── product_similarity.py    ← Product similarity graph engine
│   ├── requirements.txt         ← Backend-specific deps
│   ├── data_structures/         ← 8 custom DSA implementations
│   │   ├── bst.py               ← Binary Search Tree (price index + search trace)
│   │   ├── graph.py             ← Weighted directed graph (co-occurrence)
│   │   ├── hash_map.py          ← Hash map for O(1) lookups
│   │   ├── heap.py              ← Min-Heap (Top-K selection)
│   │   ├── linked_list.py       ← Doubly Linked List (shopping cart)
│   │   ├── queue.py             ← Bounded FIFO queue (user actions)
│   │   ├── stack.py             ← LIFO stack (view history)
│   │   └── trie.py              ← Trie / Prefix Tree (category search)
│   ├── recommendation/          ← 6-stage recommendation pipeline
│   │   ├── foolproof_pipeline.py        ← Master pipeline orchestrator
│   │   ├── collaborative_filter.py      ← Jaccard-based user similarity
│   │   ├── co_occurrence_graph.py       ← Market basket co-occurrence
│   │   ├── category_filter.py           ← Trie-based category safety filter
│   │   ├── ranking_engine.py            ← Multi-criteria scoring
│   │   └── top_k_selector.py            ← Heap-based Top-K selection
│   └── pricing/
│       └── pricing_engine.py    ← Rule-based dynamic pricing
│
├── frontend/                    ← React SPA (Vite, port 5173)
│   ├── src/
│   │   ├── App.jsx              ← Root with React Router
│   │   ├── api.js               ← Axios API client
│   │   ├── components/
│   │   │   ├── LandingPage.jsx          ← Project overview & stats
│   │   │   ├── ProductGrid.jsx          ← 89-product catalog + search/filter
│   │   │   ├── Cart.jsx                 ← Doubly linked list cart UI
│   │   │   ├── RecommendationPanel.jsx  ← Personalized recs + explainability
│   │   │   ├── UserSelectionModal.jsx   ← Choose from 20 demo users
│   │   │   ├── DSAActivityPanel.jsx     ← Real-time DSA operation feed
│   │   │   ├── DSAApplications.jsx      ← Live DSA demonstrations
│   │   │   ├── LiveDSAMonitor.jsx       ← Operation monitor overlay
│   │   │   ├── PurchaseHistory.jsx      ← User purchase timeline
│   │   │   ├── Tutorial.jsx             ← Guided walkthrough
│   │   │   ├── Animations.jsx           ← BST, Heap, Trie animations
│   │   │   └── visualizers/
│   │   │       ├── BSTVisualizer.jsx         ← Interactive BST with search trace
│   │   │       ├── GraphVisualizer.jsx        ← D3 force-directed graph
│   │   │       ├── HeapVisualizer.jsx         ← Heap array + extract-min steps
│   │   │       ├── TrieVisualizer.jsx         ← Prefix tree path highlight
│   │   │       ├── UserSimilarityGraph.jsx    ← Complete Jaccard graph (20 users)
│   │   │       └── ProductSimilarityGraph.jsx ← Product co-occurrence graph
│   │   └── App.css              ← Dark glassmorphism theme
│   └── package.json
│
├── src/                         ← Standalone Python library (no Flask needed)
│   ├── models/
│   │   ├── cart.py              ← ShoppingCart (Doubly Linked List + HashMap)
│   │   ├── session.py           ← UserSession (Stack + Queue)
│   │   └── pricing.py           ← PricingRule model
│   ├── engines/
│   │   ├── recommendation.py    ← RecommendationGraph + Personalized PageRank
│   │   ├── pricing.py           ← DynamicPricingEngine
│   │   ├── deal_selector.py     ← DealSelector (Min-Heap)
│   │   └── ecommerce_engine.py  ← Unified ECommerceEngine (all components)
│   └── utils/
│       └── knapsack.py          ← 0/1 Knapsack DP + Fractional Knapsack
│
├── app/                         ← CLI demo entry points
│   ├── main.py                  ← Full feature demo (uses src/)
│   └── interactive_demo.py      ← Interactive shopping session demo
│
├── tests/                       ← Comprehensive test suites (100+ cases)
│   ├── test_cart.py             ← 25+ cart operation tests
│   ├── test_session.py          ← 20+ session management tests
│   ├── test_pricing.py          ← 30+ pricing engine tests
│   ├── test_recommendation.py   ← 15+ recommendation tests
│   ├── test_knapsack.py         ← 20+ knapsack algorithm tests
│   ├── test_integration.py      ← 15+ end-to-end integration tests
│   ├── run_all_tests.py         ← Master test runner with report
│   └── quick_test.py            ← Interactive test selector
│
├── config/                      ← Configuration
│   ├── settings.py              ← PageRank, pricing, session, cart config
│   └── project_info.py          ← Project structure visualizer script
│
├── assets/                      ← Screenshots and media
│
└── docs/                        ← Supplementary documentation
    ├── PROJECT_SUMMARY.md       ← Detailed component descriptions
    ├── PROJECT_APPROACH_AND_SCOPE.md  ← DSA design decisions + future scope
    ├── RECOMMENDATION_ENGINE_DOCS.md  ← Recommendation pipeline deep-dive
    ├── QUICK_REFERENCE.md       ← Quick start + code examples
    ├── README_FULL.md           ← Extended academic write-up (abstract, formulas)
    ├── PROJECT_COMPLETE.txt     ← Project completion checklist
    └── archive/
        └── ecommerce_engine_core.py   ← Original monolith prototype (archived)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend language | Python 3.8+ |
| Web framework | Flask 3.0 |
| CORS | Flask-CORS 4.0 |
| Frontend framework | React 19 |
| Build tool | Vite 7 |
| Routing | React Router DOM 7 |
| HTTP client | Axios |
| Visualizations | D3.js v7 |
| Database | None — all in-memory |
| ML libraries | **None** |

---

## Data Structures Implemented

### 1. Doubly Linked List — Shopping Cart
**File:** `backend/data_structures/linked_list.py`, `src/models/cart.py`

Each cart item is a node with `prev`/`next` pointers. A companion `HashMap` (product_id → node) gives O(1) access to any item without traversal.

| Operation | Complexity |
|-----------|-----------|
| Add item | O(1) |
| Remove item | O(1) with HashMap |
| Update quantity | O(1) with HashMap |
| Get total | O(n) |

### 2. Stack — Product View History
**File:** `backend/data_structures/stack.py`

LIFO structure stores a user's recent product views. Supports push, pop (undo last view), and peek. Bounded to 20 items.

| Operation | Complexity |
|-----------|-----------|
| Push (view product) | O(1) |
| Pop (undo view) | O(1) |
| Peek (last viewed) | O(1) |

### 3. Queue — User Action Log
**File:** `backend/data_structures/queue.py`

Bounded FIFO queue (max 50) tracks user session actions in sequence (views, cart additions, etc.) for session replay and analytics.

| Operation | Complexity |
|-----------|-----------|
| Enqueue | O(1) |
| Dequeue | O(1) |

### 4. Binary Search Tree (BST) — Price Index
**File:** `backend/data_structures/bst.py`

Products indexed by price. Supports search with path tracing for visualization. A separate `viz_bst` is populated with a random 25-item subset for frontend animation.

| Operation | Complexity |
|-----------|-----------|
| Insert | O(log n) avg |
| Search with trace | O(log n) avg |
| In-order traversal (sorted) | O(n) |
| Range query | O(log n + k) |

### 5. Min-Heap — Top-K Selection
**File:** `backend/data_structures/heap.py`

Used for Top-K recommendation selection and deal prioritization. Maintains the k best candidates without sorting the entire list.

| Operation | Complexity |
|-----------|-----------|
| Push | O(log k) |
| Pop min | O(log k) |
| Top-K from N candidates | O(N log K) |

### 6. Trie (Prefix Tree) — Category & Product Search
**File:** `backend/data_structures/trie.py`

Stores all product categories and product names character-by-character. Used for O(m) prefix matching and autocomplete (m = query length).

| Operation | Complexity |
|-----------|-----------|
| Insert word | O(m) |
| Prefix search | O(m + k) |
| Autocomplete | O(m + k) |

### 7. Weighted Directed Graph — Co-Occurrence
**File:** `backend/data_structures/graph.py`, `backend/recommendation/co_occurrence_graph.py`

Products as nodes, edges weighted by how often two products appear in the same transaction. Drives "Frequently Bought Together" recommendations.

| Operation | Complexity |
|-----------|-----------|
| Add edge | O(1) |
| Get neighbors | O(deg(v)) |
| BFS/DFS traversal | O(V + E) |

### 8. Hash Map — O(1) Lookups
**File:** `backend/data_structures/hash_map.py`

Used internally for product_id → Product object, user_id → User object, and category → product list mappings throughout the system.

| Operation | Complexity |
|-----------|-----------|
| Lookup | O(1) avg |
| Insert | O(1) avg |

### 9. Product Similarity Graph
**File:** `backend/product_similarity.py`

A complete weighted undirected graph where edge weight = combined similarity score (40% Cosine + 30% Jaccard + 30% Category). Used for item-item recommendations.

---

## Algorithms Implemented

### Personalized PageRank
The core recommendation algorithm. Operates on the user-item interaction graph. Each iteration propagates scores through the network with a personalization vector biased towards the target user's interactions.

```
PR(u) = α × Σ[PR(v) / deg(v)] + (1-α) × s(u)
         v∈N(u)

where α = 0.85 (damping factor), s(u) = personalization seed
```

Runs for 20 iterations by default. O(iterations × edges).

### Jaccard Similarity — Collaborative Filtering
Measures user similarity by overlap of purchase histories.

```
J(A, B) = |A ∩ B| / |A ∪ B|

Example:
  User A purchases: {1, 2, 5, 7, 9}
  User B purchases: {2, 5, 8, 9, 11}
  J(A, B) = |{2,5,9}| / |{1,2,5,7,8,9,11}| = 3/7 ≈ 0.43
```

### 0/1 Knapsack DP — Bundle Optimization
Selects the optimal set of products to include in a bundle given a budget constraint, maximizing total value.

```
dp[i][w] = max(dp[i-1][w], dp[i-1][w - price[i]] + value[i])
Time: O(n × budget), Space: O(n × budget)
```

### Fractional Knapsack — Greedy Variant
Allows partial items. Sorts by value/weight ratio, then greedily fills the knapsack. O(n log n) for sorting.

### Combined Product Similarity
```
similarity = 0.4 × cosine_similarity
           + 0.3 × jaccard_similarity
           + 0.3 × category_match_bonus
```

---

## Recommendation Pipeline

The recommendation engine uses a **6-stage category-first pipeline**:

```
[User Action: View / Add to Cart / Purchase]
         │
         ▼
┌─────────────────────────────────────┐
│ Stage 1: Collaborative Filtering     │  Jaccard similarity across all users
│          (User-User Graph)          │  Score: collab_score × 50
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 2: Co-Occurrence Analysis      │  "People who bought X also bought Y"
│          (Weighted Graph)           │  Score: co_occurrence × 10
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 2.5: Cart Context Analysis     │  Instant boost for active cart items
│            (Immediate Intent)       │  Score: +100 cart_boost
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 3: Category Filtering          │  Trie lookup + preferred_categories
│          (Relevance Safety Layer)   │  Hard filter — wrong category = out
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 4: Multi-Criteria Ranking      │  Score = collab×50 + co_occur×10
│          (BST Price Filter)         │         + cart_boost + popularity×0.1
│                                     │         + inventory×0.05 - price×0.001
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 5: Top-K Selection             │  Min-Heap extract, O(N log K)
│          (Min-Heap)                 │  Returns top 10 recommendations
└──────────────────┬──────────────────┘
                   │
         ▼
┌─────────────────────────────────────┐
│ Stage 6: Explainability Logging      │  Full decision trace for every result
└─────────────────────────────────────┘
```

**Why category-first?** It prevents obviously irrelevant suggestions (e.g., recommending beauty products to someone shopping for programming books) by using the user's `preferred_categories` set as a hard filter before any scoring.

**Cold-start handling:** New users with no history see globally popular items (PageRank-style scoring without personalization).

---

## Dynamic Pricing Engine

**File:** `backend/pricing/pricing_engine.py`

Rule-based pricing — no regression models. Four rule types applied in priority order:

| Rule | Condition | Effect |
|------|-----------|--------|
| Low Stock | inventory < 10 | price × 1.15 (+15%) |
| High Demand | views > avg × 2 | price × (1 + 0.1 × normalized_views) |
| Cart Abandonment | item in cart > 24h | price × 0.90 (−10%) |
| Loyalty | user purchases > 5 | price × 0.95 (−5%) |

Combined formula:
```
Final_Price = base × demand_mult × inventory_mult × loyalty_disc × flash_disc
```

User segments also affect price:
- `premium` → ×0.95 (5% discount)
- `normal` → ×1.00
- `budget` → ×1.05 (5% markup)
- `vip` → ×0.90 (10% discount)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | System health check |
| GET | `/api/products` | All products (filter: `?category=`, `?q=`) |
| GET | `/api/products/:id` | Single product |
| GET | `/api/users` | All 20 demo users |
| GET | `/api/users/:id` | Single user |
| GET | `/api/recommendations/:userId` | Personalized recommendations (`?k=10&explain=true`) |
| GET | `/api/recommendations/:userId/explain/:productId` | Explain a specific recommendation |
| GET | `/api/frequently-bought-together/:productId` | Co-occurrence based suggestions |
| GET | `/api/pricing/:productId` | Dynamic price with breakdown |
| POST | `/api/cart/:userId/add` | Add item to cart |
| GET | `/api/cart/:userId` | Get cart contents |
| POST | `/api/cart/:userId/remove` | Remove item |
| POST | `/api/cart/:userId/update-quantity` | Update item quantity |
| POST | `/api/cart/:userId/clear` | Clear cart |
| POST | `/api/checkout/:userId` | Complete purchase |
| POST | `/api/view/:userId/:productId` | Track product view |
| GET | `/api/recent-views/:userId` | User's view stack |
| GET | `/api/categories` | All product categories |
| GET | `/api/dsa-activity` | Recent DSA operations log |
| POST | `/api/dsa-activity/log` | Log frontend DSA activity |
| GET | `/api/stats` | System statistics |
| GET | `/api/visualize/bst/structure` | BST structure (25 nodes) |
| GET | `/api/visualize/bst/search?price=X` | BST search trace |
| GET | `/api/visualize/bst/sort` | In-order sorted products |
| GET | `/api/visualize/heap/extract-min` | Heap sort steps |
| GET | `/api/visualize/trie/search?q=X` | Trie prefix trace |
| GET | `/api/visualize/recommendation-graph/:userId` | Cart-based rec graph |
| GET | `/api/visualize/user-product-graph/:userId` | User-product bipartite graph |
| GET | `/api/visualize/user-similarity-graph` | Complete Jaccard graph |
| GET | `/api/visualize/user-orders/:userId` | Order history graph |
| GET | `/api/visualize/product-similarity-graph` | Product similarity graph |

---

## How to Run

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Option 1 — Automated (Recommended)

```powershell
# From the project root
.\start.ps1
```

This starts both the backend (port 5000) and frontend (port 5173) servers automatically.

### Option 2 — Manual

**Step 1: Start the backend**

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

The Flask server starts at `http://localhost:5000`

**Step 2: Start the frontend**

```powershell
cd frontend
npm install
npm run dev
```

The React app starts at `http://localhost:5173`

**Step 3: Open the app**

Navigate to `http://localhost:5173` in your browser.

### Option 3 — CLI Demo Only (no web server needed)

```powershell
# Install minimal dependencies
pip install -r requirements.txt

# Run the full feature demo
python app/main.py

# Run the interactive shopping demo
python app/interactive_demo.py

# Use the helper menu
python run.py

# View project structure
python config/project_info.py
```

### Running Tests

```powershell
# Run all 100+ tests with report
python tests/run_all_tests.py

# Run specific test suites
python tests/test_cart.py
python tests/test_session.py
python tests/test_pricing.py
python tests/test_recommendation.py
python tests/test_knapsack.py
python tests/test_integration.py

# Interactive test selector
python tests/quick_test.py
```

---

## Data

All data is in-memory (no database required), seeded at startup from `backend/sample_data.py`.

- **89 Products** across 10 categories:
  Electronics, Home & Kitchen, Fashion, Books, Sports & Fitness,
  Beauty & Personal Care, Toys & Games, Automotive, Office Supplies, Health & Wellness

- **20 Users** (U001–U020): Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Henry, Iris, Jack,
  Kate, Leo, Mia, Noah, Olivia, Paul, Quinn, Rachel, Sam, Tina

- **100 Transactions** with realistic affinity groups (e.g., Apple ecosystem bundles,
  home office setups, fitness bundles) plus 30 random transactions for diversity

- **All carts start empty** — intentional design so demo interactions drive recommendations

---

## Frontend Features

### Pages & Components

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | `LandingPage` | Project overview, stats, quick-start guide |
| `/products` | `ProductGrid` | Browse 89 products, search, category filter |
| `/cart` | `Cart` | Doubly linked list cart with quantity controls |
| `/recommendations` | `RecommendationPanel` | Personalized recs with full explainability |
| `/dsa` | `DSAApplications` | Live DSA demonstrations with real data |
| `/visualize/bst` | `BSTVisualizer` | Interactive BST — insert, search, traverse |
| `/visualize/heap` | `HeapVisualizer` | Heap array + extract-min animation |
| `/visualize/trie` | `TrieVisualizer` | Prefix search path highlight |
| `/visualize/graph` | `GraphVisualizer` | D3 force-directed co-occurrence graph |
| `/visualize/similarity` | `ProductSimilarityGraph` | Product similarity network |
| `/visualize/users` | `UserSimilarityGraph` | Complete Jaccard similarity graph |

### Real-time DSA Activity Panel

Every API call logs the DSA operation it performs (e.g., `PUSH → Stack`, `INSERT → Doubly Linked List`, `HEAP EXTRACT → Min-Heap`). The `DSAActivityPanel` component polls `/api/dsa-activity` and shows a live feed of operations, making the invisible internals visible.

### Design System

- Dark theme with vibrant gradient accents
- Glassmorphism cards
- Smooth CSS transitions and micro-interactions
- Responsive layout
- Toast notifications for cart/action feedback

---

## CLI Demo (Python-only)

The `src/` library and `app/` demos run without Flask or React. They demonstrate the same DSA concepts through a terminal interface.

### Quick Example

```python
from src.engines.ecommerce_engine import ECommerceEngine

engine = ECommerceEngine(damping_factor=0.85, pagerank_iterations=20)

# Configure pricing rules
engine.pricing_engine.add_pricing_rule(min_inv=0,  max_inv=10,  multiplier=1.15, priority=1)
engine.pricing_engine.add_pricing_rule(min_inv=11, max_inv=50,  multiplier=1.0,  priority=2)
engine.pricing_engine.add_pricing_rule(min_inv=51, max_inv=100, multiplier=0.90, priority=3)

# Set up a product
engine.pricing_engine.set_base_price(101, 1000)
engine.pricing_engine.update_inventory(101, 5)   # Low stock

# Simulate user journey
engine.create_user(1, "premium")
engine.track_view(1, 101)
engine.track_view(1, 102)
engine.track_purchase(1, 101)

# Get recommendations (Personalized PageRank)
recs = engine.get_recommendations(1, k=5)
for product_id, score in recs:
    print(f"Product {product_id}: score={score:.4f}")

# Dynamic pricing
breakdown = engine.get_price_breakdown(101, 1)
print(f"Final price: Rs. {breakdown['final_price']:.2f}")  # Low stock premium applied

# Cart operations
engine.add_to_cart(1, 101, quantity=2)
cart = engine.get_cart_summary(1)
print(f"Cart total: Rs. {cart['total']:.2f}")

# Bundle optimization (0/1 Knapsack)
engine.deal_selector.add_deal(101, 1000, 10)
engine.deal_selector.add_deal(102, 500, 15)
bundle = engine.optimize_bundle(1, max_budget=1200)
print(f"Optimal bundle: {bundle['bundle']}")
```

---

## Complexity Analysis

| Operation | Data Structure | Algorithm | Time Complexity |
|-----------|---------------|-----------|-----------------|
| Add to cart | Doubly Linked List + HashMap | — | O(1) |
| Remove from cart | Doubly Linked List + HashMap | — | O(1) |
| Track product view | Stack | Push | O(1) |
| Log user action | Queue | Enqueue | O(1) |
| Price lookup | HashMap | — | O(1) |
| Product by ID | HashMap | — | O(1) |
| Price range query | BST | Range search | O(log n + k) |
| Category search | Trie | Prefix match | O(m + k) |
| Top-K recommendations | Min-Heap | Extract-min × K | O(N log K) |
| Add deal | Min-Heap | Heappush | O(log k) |
| Collaborative filter | Graph | Jaccard pairwise | O(U × P) |
| Co-occurrence lookup | Graph | BFS | O(V + E) |
| PageRank | Graph | Iterative | O(iter × E) |
| Bundle optimization | DP table | Knapsack | O(n × budget) |
| Dynamic pricing | Rule list | Linear scan | O(k rules) |
| **Full pipeline** | **Combined** | **6-stage** | **O(U×P + E + N log K)** |

---

## Mathematical Formulations

### Personalized PageRank
```
PR(u) = α × Σ [PR(v) / deg(v)] + (1 - α) × s(u)
             v ∈ N(u)

α = 0.85 (damping factor)
s(u) = personalization vector (biased toward target user's interactions)
```

### Jaccard Similarity
```
J(A, B) = |A ∩ B| / |A ∪ B|
```

### Product Similarity Score
```
sim(p1, p2) = 0.4 × cos(p1, p2) + 0.3 × J(p1, p2) + 0.3 × category_match
```

### Recommendation Score (Multi-Criteria Ranking)
```
Score = collab_score × 50
      + co_occurrence_score × 10
      + cart_boost (100 if related to cart item, else 0)
      + popularity × 0.1
      + inventory_level × 0.05
      − price × 0.001
```

### Dynamic Pricing
```
Final_Price = base_price
            × inventory_multiplier   (1.15 / 1.00 / 0.90)
            × demand_multiplier      (1.0 + 0.1 × normalized_views)
            × loyalty_discount       (0.95 if purchases > 5)
            × segment_multiplier     (0.90–1.05)
```

### 0/1 Knapsack DP
```
dp[i][w] = max(dp[i-1][w],  dp[i-1][w - price[i]] + value[i])
           ↑ skip item i     ↑ include item i (if budget allows)

Time: O(n × W),  Space: O(n × W)
n = number of products, W = max budget
```

---

## Future Scope

Identified data structures and enhancements for future implementation:

| Advanced Structure | Purpose | Benefit |
|-------------------|---------|---------|
| AVL / Red-Black Tree | Self-balancing BST for live price updates | Guaranteed O(log n) worst case |
| B-Tree / B+ Tree | Disk-optimized product index | Scalable to millions of products |
| Bloom Filter | Probabilistic "seen this product?" check | Massive memory saving for cache |
| K-D Tree | Multi-attribute nearest-neighbor search | Filter by price + rating + size simultaneously |
| Segment Tree | Price range statistics | O(log n) range aggregation |
| LRU Cache | Doubly Linked List + HashMap eviction | O(1) cache for hot product data |
| Skip List | Sorted products with simpler balancing | Probabilistic O(log n), easier concurrent access |
| Suffix Tree | Fuzzy product name search | Typo-tolerant autocomplete |
| DSU / Union-Find | Product clustering and category merging | Near-constant time group operations |
| Persistent DS | Cart history, undo/redo, A/B snapshots | Time-travel queries |

---

## Project Statistics

| Metric | Count |
|--------|-------|
| Custom data structure implementations | 9 |
| Recommendation pipeline stages | 6 |
| API endpoints | 30+ |
| React components | 20+ |
| Products in catalog | 89 |
| Demo users | 20 |
| Transactions (training data) | 100 |
| Python source files | 30+ |
| Test cases | 100+ |
| Total lines of code | ~5,000 |
| ML/AI libraries used | **0** |

---

## Dependencies

### Backend (`backend/requirements.txt`)
```
Flask==3.0.0
Flask-CORS==4.0.0
```

That's it. No ML frameworks, no ORMs, no external algorithm libraries.

### Frontend (`frontend/package.json`)
```
react ^19.2.0
react-dom ^19.2.0
react-router-dom ^7.12.0
axios ^1.13.2
d3 ^7.9.0
vite ^7.2.4
```

---

## Supplementary Docs

All additional documentation lives in `docs/`:

| File | Contents |
|------|----------|
| `docs/PROJECT_SUMMARY.md` | Detailed breakdown of every component with code examples |
| `docs/PROJECT_APPROACH_AND_SCOPE.md` | Design decisions, all 9 DSA implementations, and 12 future data structures |
| `docs/RECOMMENDATION_ENGINE_DOCS.md` | Deep-dive into the 6-stage pipeline with Mermaid diagram |
| `docs/QUICK_REFERENCE.md` | Quick-start commands and copy-paste code snippets |
| `docs/README_FULL.md` | Full academic write-up with abstract, formulas, and complexity tables |
| `docs/PROJECT_COMPLETE.txt` | Project completion checklist |
| `docs/archive/ecommerce_engine_core.py` | Original monolithic prototype (kept for reference) |

---

## Authors

DSA Lab Team — Academic Project, RVCE

## License

Academic Project — DSA Implementation Demonstration

---

*Built with classical algorithms, not machine learning. Every recommendation is explainable.* 🎓
