"""
Bundle Optimization using 0/1 Knapsack Dynamic Programming
Maximizes value within a budget constraint
"""

from typing import List, Tuple, Dict


def bundle_optimization(
    products: List[Tuple[int, float]],
    max_budget: float
) -> List[int]:
    """
    0/1 Knapsack DP: Select products to maximize value within budget.
    
    Problem: Given products with prices, select subset that maximizes
    total value without exceeding budget.
    
    Time Complexity: O(n * budget)
    Space Complexity: O(n * budget)
    
    Args:
        products: List of tuples (product_id, price)
        max_budget: Maximum budget constraint
        
    Returns:
        List of product_ids in optimal bundle
    """
    if not products or max_budget <= 0:
        return []

    n = len(products)
    budget_int = int(max_budget)
    
    # DP table: dp[i][w] = max value using first i products with budget w
    dp = [[0.0] * (budget_int + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        prod_id, price = products[i - 1]
        price_int = int(price)
        
        for w in range(budget_int + 1):
            # Option 1: Don't include this product
            dp[i][w] = dp[i - 1][w]

            # Option 2: Include this product (if budget allows)
            if price_int <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - price_int] + price
                )

    # Backtrack to find which products were selected
    bundle = []
    w = budget_int
    
    for i in range(n, 0, -1):
        # Check if this product was included
        if dp[i][w] != dp[i - 1][w]:
            prod_id, price = products[i - 1]
            bundle.append(prod_id)
            w -= int(price)

    return bundle


def bundle_optimization_with_weights(
    products: List[Tuple[int, float, float]],
    max_budget: float
) -> Dict:
    """
    Enhanced 0/1 Knapsack with separate value and cost.
    
    Args:
        products: List of tuples (product_id, value, cost)
        max_budget: Maximum budget constraint
        
    Returns:
        Dictionary with bundle details
    """
    if not products or max_budget <= 0:
        return {
            "bundle": [],
            "total_value": 0,
            "total_cost": 0,
            "budget_remaining": max_budget
        }

    n = len(products)
    budget_int = int(max_budget)
    
    # DP table
    dp = [[0.0] * (budget_int + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        prod_id, value, cost = products[i - 1]
        cost_int = int(cost)
        
        for w in range(budget_int + 1):
            dp[i][w] = dp[i - 1][w]
            
            if cost_int <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - cost_int] + value
                )

    # Backtrack
    bundle = []
    total_value = 0
    total_cost = 0
    w = budget_int
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            prod_id, value, cost = products[i - 1]
            bundle.append(prod_id)
            total_value += value
            total_cost += cost
            w -= int(cost)

    return {
        "bundle": bundle,
        "total_value": total_value,
        "total_cost": total_cost,
        "budget_remaining": max_budget - total_cost,
        "efficiency": total_value / total_cost if total_cost > 0 else 0
    }


def fractional_knapsack(
    products: List[Tuple[int, float, float]],
    max_budget: float
) -> Dict:
    """
    Fractional Knapsack (Greedy): Can take fractions of items.
    Useful for scenarios where partial purchase is allowed.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        products: List of tuples (product_id, value, cost)
        max_budget: Maximum budget constraint
        
    Returns:
        Dictionary with bundle details including fractions
    """
    if not products or max_budget <= 0:
        return {
            "bundle": [],
            "total_value": 0,
            "total_cost": 0
        }

    # Calculate value-to-cost ratio
    items = []
    for prod_id, value, cost in products:
        if cost > 0:
            ratio = value / cost
            items.append((prod_id, value, cost, ratio))

    # Sort by ratio (descending)
    items.sort(key=lambda x: x[3], reverse=True)

    bundle = []
    total_value = 0
    total_cost = 0
    remaining_budget = max_budget

    for prod_id, value, cost, ratio in items:
        if remaining_budget >= cost:
            # Take full item
            bundle.append((prod_id, 1.0))  # (product_id, fraction)
            total_value += value
            total_cost += cost
            remaining_budget -= cost
        elif remaining_budget > 0:
            # Take fraction
            fraction = remaining_budget / cost
            bundle.append((prod_id, fraction))
            total_value += value * fraction
            total_cost += cost * fraction
            remaining_budget = 0
            break

    return {
        "bundle": bundle,
        "total_value": total_value,
        "total_cost": total_cost,
        "budget_remaining": max_budget - total_cost
    }
