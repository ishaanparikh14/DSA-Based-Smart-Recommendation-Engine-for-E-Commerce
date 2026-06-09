"""
Configuration settings for E-Commerce Engine
"""

# Recommendation Engine Settings
RECOMMENDATION_CONFIG = {
    "damping_factor": 0.85,
    "pagerank_iterations": 20,
    "default_top_k": 5
}

# Pricing Engine Settings
PRICING_CONFIG = {
    "segment_multipliers": {
        "premium": 0.95,    # 5% discount
        "normal": 1.0,      # No change
        "budget": 1.05,     # 5% markup
        "vip": 0.90        # 10% discount
    },
    "default_pricing_rules": [
        {
            "name": "Low Stock Premium",
            "min_inv": 0,
            "max_inv": 10,
            "multiplier": 1.15,
            "priority": 1
        },
        {
            "name": "Normal Stock",
            "min_inv": 11,
            "max_inv": 50,
            "multiplier": 1.0,
            "priority": 2
        },
        {
            "name": "High Stock Discount",
            "min_inv": 51,
            "max_inv": 100,
            "multiplier": 0.90,
            "priority": 3
        }
    ]
}

# Session Settings
SESSION_CONFIG = {
    "max_recent_actions": 10,
    "session_timeout": 1800,  # 30 minutes
    "idle_warning_threshold": 600  # 10 minutes
}

# Cart Settings
CART_CONFIG = {
    "max_items_per_product": 99,
    "max_cart_items": 50
}

# Deal Selector Settings
DEAL_CONFIG = {
    "top_deals_count": 5,
    "min_discount_percent": 5.0
}

# System Settings
SYSTEM_CONFIG = {
    "debug_mode": False,
    "log_level": "INFO",
    "max_users": 10000
}
