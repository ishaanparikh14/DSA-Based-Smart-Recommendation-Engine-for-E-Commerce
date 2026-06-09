import { useState, useEffect } from 'react';
import { getCart, removeFromCart, updateCartQuantity, getProducts, getFrequentlyBoughtTogether } from '../api';
import axios from 'axios'; // Added axios import
import GraphVisualizer from './visualizers/GraphVisualizer';

function Cart({ currentUser, setCartCount }) {
    const [cart, setCart] = useState({ items: [], total: 0, size: 0 }); // Initial state for cart
    const [loading, setLoading] = useState(true);
    const [productMap, setProductMap] = useState({});
    const [checkingOut, setCheckingOut] = useState(false); // New state for checkout loading
    const [toast, setToast] = useState(null); // New state for toast messages
    const [showGraph, setShowGraph] = useState(true); // State for graph visualization toggle
    const [recommendations, setRecommendations] = useState([]); // Frequently bought together items
    const [loadingRecommendations, setLoadingRecommendations] = useState(false);

    // Helper function for showing toasts (assuming it's defined elsewhere or needs to be added)
    // For now, we'll just console.log if showToast isn't defined.
    const showToast = (message, type) => {
        console.log(`Toast (${type}): ${message}`);
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    // Helper function to get product initials
    const getProductInitials = (name) => {
        if (!name) return '?';
        const words = name.split(' ');
        if (words.length >= 2) {
            return (words[0][0] + words[1][0]).toUpperCase();
        }
        return name.substring(0, Math.min(3, name.length)).toUpperCase();
    };

    // Helper function to convert category to CSS class name
    const getCategoryClass = (category) => {
        if (!category) return 'placeholder-electronics';
        return 'placeholder-' + category.toLowerCase().replace(/\s+/g, '-').replace(/&/g, '');
    };

    useEffect(() => {
        if (currentUser) { // Added condition for currentUser
            loadCart();
            loadProducts();
        }

        // Listen for cart updates from other components
        const handleCartUpdate = () => {
            console.log('Cart update event received, reloading cart...');
            loadCart();
        };
        
        window.addEventListener('cartUpdated', handleCartUpdate);
        
        return () => {
            window.removeEventListener('cartUpdated', handleCartUpdate);
        };
    }, [currentUser]);

    const loadProducts = async () => {
        try {
            const response = await getProducts();
            const map = {};
            response.data.forEach((p) => {
                map[p.id] = p;
            });
            setProductMap(map);
        } catch (error) {
            console.error('Error loading products:', error);
            showToast('Error loading product details', 'error'); // Added toast
        }
    };

    const loadCart = async () => {
        if (!currentUser) return;

        try {
            setLoading(true);
            const response = await getCart(currentUser.id);
            setCart(response.data);
            setCartCount(response.data.size || 0);
            
            // Load recommendations based on cart items
            if (response.data.items && response.data.items.length > 0) {
                loadRecommendations(response.data.items);
            } else {
                // Clear recommendations if cart is empty
                setRecommendations([]);
            }
        } catch (error) {
            console.error('Error loading cart:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadRecommendations = async (cartItems) => {
        try {
            console.log('Loading recommendations for cart items:', cartItems);
            setLoadingRecommendations(true);
            setRecommendations([]); // Clear old recommendations first
            const allRecommendations = new Map();
            
            // Get frequently bought together items for each cart item
            for (const item of cartItems) {
                try {
                    console.log('Fetching recommendations for product:', item.product_id);
                    const response = await getFrequentlyBoughtTogether(item.product_id, 5);
                    console.log('Recommendations response:', response.data);
                    
                    // Backend returns: { product_id, frequently_bought_together: [{product_id, co_occurrence_score, product}] }
                    if (response.data && response.data.frequently_bought_together && response.data.frequently_bought_together.length > 0) {
                        response.data.frequently_bought_together.forEach(item => {
                            if (item.product) {
                                const rec = {
                                    ...item.product,
                                    co_occurrence_score: item.co_occurrence_score
                                };
                                
                                // Don't recommend items already in cart
                                const isInCart = cartItems.some(ci => ci.product_id === rec.id);
                                if (!isInCart) {
                                    // Use Map to avoid duplicates, keep highest co-occurrence score
                                    if (!allRecommendations.has(rec.id) || 
                                        allRecommendations.get(rec.id).co_occurrence_score < rec.co_occurrence_score) {
                                        allRecommendations.set(rec.id, rec);
                                    }
                                }
                            }
                        });
                    }
                } catch (err) {
                    console.error(`Error fetching recommendations for product ${item.product_id}:`, err);
                }
            }
            
            // Convert to array and sort by co-occurrence score
            const sortedRecs = Array.from(allRecommendations.values())
                .sort((a, b) => b.co_occurrence_score - a.co_occurrence_score)
                .slice(0, 6); // Limit to top 6
                
            console.log('Final recommendations:', sortedRecs);
            setRecommendations(sortedRecs);
        } catch (error) {
            console.error('Error loading recommendations:', error);
        } finally {
            setLoadingRecommendations(false);
        }
    };

    const handleUpdateQuantity = async (productId, newQuantity) => {
        try {
            const id = parseInt(productId, 10);
            await updateCartQuantity(currentUser.id, id, newQuantity);
            loadCart();
        } catch (error) {
            console.error('Error updating quantity:', error);
            showToast('Error updating quantity', 'error');
        }
    };

    const handleRemove = async (productId) => {
        try {
            // Ensure productId is an integer
            const id = parseInt(productId, 10);
            await removeFromCart(currentUser.id, id);
            loadCart();
        } catch (error) {
            console.error('Error removing from cart:', error);
            showToast('Error removing item', 'error');
        }
    };

    const handleAddRecommendation = async (productId) => {
        try {
            const axios = (await import('axios')).default;
            await axios.post(`http://localhost:5000/api/cart/${currentUser.id}/add`, {
                product_id: productId,
                quantity: 1
            });
            showToast('✅ Added to cart!', 'success');
            await loadCart(); // Reload cart to update with await
        } catch (error) {
            console.error('Error adding recommendation to cart:', error);
            showToast('Error adding item', 'error');
        }
    };

    const handleCheckout = async () => {
        if (!cart || cart.size === 0) {
            showToast('Cart is empty!', 'error');
            return;
        }

        try {
            setCheckingOut(true);

            // Extract product IDs for the backend
            const productIds = cart.items.map(item => item.product_id);

            // Call checkout endpoint with product_ids payload
            await axios.post(`http://localhost:5000/api/checkout/${currentUser.id}`, {
                product_ids: productIds
            });

            showToast('Order placed successfully! 🎉', 'success');
            
            // Dispatch event to notify other components (like graphs) to refresh
            window.dispatchEvent(new CustomEvent('checkoutComplete', { 
                detail: { userId: currentUser.id, productIds } 
            }));

            // Reload cart and update count
            setTimeout(() => {
                loadCart();
                setCartCount(0);
            }, 1500);
        } catch (error) {
            console.error('Error during checkout:', error);
            showToast('Checkout failed. Please try again.', 'error');
        } finally {
            setCheckingOut(false);
        }
    };

    if (loading) {
        return <div className="spinner"></div>;
    }

    if (cart.items.length === 0) {
        return (
            <div className="glass-card text-center" style={{ padding: '3rem' }}>
                <h2>Your cart is empty</h2>
                <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
                    Add some products to get started!
                </p>
            </div>
        );
    }

    return (
        <div>
            <h1 style={{ marginBottom: '2rem' }}>Shopping Cart</h1>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
                {/* Cart Items */}
                <div>
                    <div className="glass-card">
                        <h3 style={{ marginBottom: '1.5rem' }}>
                            Cart Items ({cart.size})
                        </h3>

                        {cart.items.map((item) => {
                            const product = productMap[item.product_id];
                            return (
                                <div
                                    key={item.product_id}
                                    style={{
                                        display: 'flex',
                                        gap: '1rem',
                                        padding: '1rem',
                                        background: 'var(--bg-secondary)',
                                        borderRadius: '8px',
                                        marginBottom: '1rem',
                                        alignItems: 'center',
                                    }}
                                >
                                    {product && (
                                        <>
                                            {product.image_url ? (
                                                <div
                                                    style={{
                                                        width: '80px',
                                                        height: '80px',
                                                        borderRadius: '8px',
                                                        overflow: 'hidden',
                                                        background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                    }}
                                                >
                                                    <img
                                                        src={product.image_url}
                                                        alt={item.product_name}
                                                        style={{
                                                            width: '100%',
                                                            height: '100%',
                                                            objectFit: 'contain',
                                                            padding: '5px',
                                                        }}
                                                        onError={(e) => {
                                                            e.target.style.display = 'none';
                                                            e.target.parentElement.innerHTML = `<div class="product-placeholder ${getCategoryClass(product.category)}" style="width: 80px; height: 80px; border-radius: 8px; font-size: 1.5rem;">${getProductInitials(item.product_name)}</div>`;
                                                        }}
                                                    />
                                                </div>
                                            ) : (
                                                <div
                                                    className={`product-placeholder ${getCategoryClass(product.category)}`}
                                                    style={{
                                                        width: '80px',
                                                        height: '80px',
                                                        borderRadius: '8px',
                                                        fontSize: '1.5rem',
                                                    }}
                                                >
                                                    {getProductInitials(item.product_name)}
                                                </div>
                                            )}
                                        </>
                                    )}

                                    <div style={{ flex: 1 }}>
                                        <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                                            {item.product_name}
                                        </div>
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                            {item.product_category}
                                        </div>
                                        <div style={{ marginTop: '0.5rem' }}>
                                            <span style={{ color: 'var(--primary)', fontWeight: 600 }}>
                                                ${item.price.toFixed(2)}
                                            </span>
                                        </div>
                                        <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Quantity:</span>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                                <button
                                                    className="btn btn-secondary"
                                                    style={{ 
                                                        fontSize: '1rem', 
                                                        padding: '0.25rem 0.5rem',
                                                        minWidth: '32px',
                                                        height: '32px'
                                                    }}
                                                    onClick={() => handleUpdateQuantity(item.product_id, Math.max(0, item.quantity - 1))}
                                                >
                                                    −
                                                </button>
                                                <span style={{ 
                                                    fontWeight: 600, 
                                                    fontSize: '1rem',
                                                    minWidth: '30px',
                                                    textAlign: 'center'
                                                }}>
                                                    {item.quantity}
                                                </span>
                                                <button
                                                    className="btn btn-secondary"
                                                    style={{ 
                                                        fontSize: '1rem', 
                                                        padding: '0.25rem 0.5rem',
                                                        minWidth: '32px',
                                                        height: '32px'
                                                    }}
                                                    onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                                                >
                                                    +
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <div style={{ textAlign: 'right' }}>
                                        <div style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                                            ${item.subtotal.toFixed(2)}
                                        </div>
                                        <button
                                            className="btn btn-secondary"
                                            style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}
                                            onClick={() => handleRemove(item.product_id)}
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>

                    {/* Users Also Purchase Section */}
                    <div className="glass-card mt-2">
                        <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            💡 Users also purchase...
                        </h3>
                        {recommendations.length === 0 && !loadingRecommendations && (
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                                No recommendations available for items in your cart
                            </p>
                        )}
                        {recommendations.length > 0 && (
                            <>
                            <h3 style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                💡 Users also purchase...
                            </h3>
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                                Frequently bought together with items in your cart
                            </p>
                            <div style={{ 
                                fontSize: '0.8rem', 
                                padding: '0.75rem', 
                                background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%)',
                                borderRadius: '6px',
                                border: '1px solid rgba(99, 102, 241, 0.2)',
                                marginBottom: '1rem'
                            }}>
                                <strong>🎯 PageRank Algorithm:</strong> Products ranked by co-occurrence score using graph-based collaborative filtering
                            </div>
                            
                            {loadingRecommendations ? (
                                <div style={{ textAlign: 'center', padding: '2rem' }}>
                                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                                </div>
                            ) : (
                                <div style={{ 
                                    display: 'grid', 
                                    gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', 
                                    gap: '1rem' 
                                }}>
                                    {recommendations.map((rec, index) => (
                                        <div
                                            key={rec.id}
                                            style={{
                                                background: 'var(--bg-secondary)',
                                                borderRadius: '8px',
                                                padding: '1rem',
                                                border: '1px solid var(--border-color)',
                                                transition: 'transform 0.2s, box-shadow 0.2s',
                                                cursor: 'pointer',
                                                position: 'relative',
                                            }}
                                            onMouseEnter={(e) => {
                                                e.currentTarget.style.transform = 'translateY(-4px)';
                                                e.currentTarget.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.3)';
                                            }}
                                            onMouseLeave={(e) => {
                                                e.currentTarget.style.transform = 'translateY(0)';
                                                e.currentTarget.style.boxShadow = 'none';
                                            }}
                                        >
                                            {/* Rank Badge */}
                                            <div style={{
                                                position: 'absolute',
                                                top: '0.5rem',
                                                left: '0.5rem',
                                                background: index < 3 ? 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                                color: 'white',
                                                width: '28px',
                                                height: '28px',
                                                borderRadius: '50%',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '0.8rem',
                                                fontWeight: '700',
                                                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
                                                zIndex: 1,
                                            }}>
                                                #{index + 1}
                                            </div>
                                            {rec.image_url ? (
                                                <div
                                                    style={{
                                                        width: '100%',
                                                        height: '100px',
                                                        borderRadius: '6px',
                                                        marginBottom: '0.75rem',
                                                        overflow: 'hidden',
                                                        background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                    }}
                                                >
                                                    <img
                                                        src={rec.image_url}
                                                        alt={rec.name}
                                                        style={{
                                                            width: '100%',
                                                            height: '100%',
                                                            objectFit: 'contain',
                                                            padding: '5px',
                                                        }}
                                                        onError={(e) => {
                                                            e.target.style.display = 'none';
                                                            const placeholder = document.createElement('div');
                                                            placeholder.className = `product-placeholder ${getCategoryClass(rec.category)}`;
                                                            placeholder.style.cssText = 'width: 100%; height: 100px; border-radius: 6px; margin-bottom: 0.75rem; font-size: 1.2rem; display: flex; align-items: center; justify-content: center;';
                                                            placeholder.textContent = getProductInitials(rec.name);
                                                            e.target.parentElement.replaceWith(placeholder);
                                                        }}
                                                    />
                                                </div>
                                            ) : (
                                                <div
                                                    className={`product-placeholder ${getCategoryClass(rec.category)}`}
                                                    style={{
                                                        width: '100%',
                                                        height: '100px',
                                                        borderRadius: '6px',
                                                        marginBottom: '0.75rem',
                                                        fontSize: '1.2rem',
                                                    }}
                                                >
                                                    {getProductInitials(rec.name)}
                                                </div>
                                            )}
                                            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem', lineHeight: '1.3' }}>
                                                {rec.name.length > 40 ? rec.name.substring(0, 40) + '...' : rec.name}
                                            </div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                                                {rec.category}
                                            </div>
                                            <div style={{ 
                                                display: 'flex', 
                                                flexDirection: 'column',
                                                gap: '0.5rem',
                                                marginBottom: '0.75rem' 
                                            }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                    <span style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '1.1rem' }}>
                                                        ${rec.price.toFixed(2)}
                                                    </span>
                                                    <span style={{ 
                                                        fontSize: '0.7rem', 
                                                        padding: '3px 8px', 
                                                        background: 'rgba(99, 102, 241, 0.2)',
                                                        borderRadius: '4px',
                                                        color: '#818cf8',
                                                        fontWeight: '600'
                                                    }}>
                                                        {Math.round(rec.co_occurrence_score * 100)}% match
                                                    </span>
                                                </div>
                                                <div style={{ 
                                                    fontSize: '0.7rem', 
                                                    padding: '4px 8px', 
                                                    background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%)',
                                                    borderRadius: '4px',
                                                    color: 'var(--text-primary)',
                                                    border: '1px solid rgba(168, 85, 247, 0.3)',
                                                    textAlign: 'center',
                                                    fontWeight: '600'
                                                }}>
                                                    📊 Score: {rec.co_occurrence_score.toFixed(4)}
                                                </div>
                                            </div>
                                            <button
                                                className="btn btn-primary"
                                                style={{ width: '100%', padding: '0.5rem', fontSize: '0.85rem' }}
                                                onClick={() => handleAddRecommendation(rec.id)}
                                            >
                                                � Add to Cart
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                            </>
                        )}
                    </div>

                    {/* Linked List Visualization */}
                    <div className="glass-card mt-2">
                        <h3 style={{ marginBottom: '1rem' }}>
                            🔗 Doubly Linked List Visualization
                        </h3>
                        <div style={{ overflowX: 'auto', padding: '1rem 0' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', minWidth: 'max-content' }}>
                                <div
                                    style={{
                                        padding: '0.5rem 1rem',
                                        background: 'var(--bg-secondary)',
                                        borderRadius: '8px',
                                        border: '2px solid var(--primary)',
                                        fontWeight: 600,
                                    }}
                                >
                                    HEAD
                                </div>

                                {cart.items.map((item, index) => (
                                    <div key={item.product_id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <span style={{ color: 'var(--primary)' }}>⟷</span>
                                        <div
                                            style={{
                                                padding: '1rem',
                                                background: 'var(--bg-secondary)',
                                                borderRadius: '8px',
                                                border: '1px solid var(--border-color)',
                                                minWidth: '150px',
                                            }}
                                        >
                                            <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                                                {item.product_name?.substring(0, 20)}...
                                            </div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                                                Qty: {item.quantity}
                                            </div>
                                        </div>
                                    </div>
                                ))}

                                <span style={{ color: 'var(--primary)' }}>⟷</span>
                                <div
                                    style={{
                                        padding: '0.5rem 1rem',
                                        background: 'var(--bg-secondary)',
                                        borderRadius: '8px',
                                        border: '2px solid var(--primary)',
                                        fontWeight: 600,
                                    }}
                                >
                                    TAIL
                                </div>
                            </div>
                        </div>
                        <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            Each node contains: product_id, quantity, price, prev pointer, next pointer
                        </div>
                    </div>

                    {/* Recommendation Graph Visualization */}
                    <div className="glass-card mt-2">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h3 style={{ margin: 0 }}>
                                📊 Recommendation Graph
                            </h3>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setShowGraph(!showGraph)}
                                style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                            >
                                {showGraph ? '🔽 Hide' : '🔼 Show'}
                            </button>
                        </div>
                        {showGraph && (
                            <GraphVisualizer
                                userId={currentUser?.id}
                                cartItems={cart.items}
                            />
                        )}
                    </div>
                </div>

                {/* Order Summary */}
                <div>
                    <div className="glass-card" style={{ position: 'sticky', top: '100px' }}>
                        <h3 style={{ marginBottom: '1.5rem' }}>Order Summary</h3>

                        <div style={{ marginBottom: '1rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                <span style={{ color: 'var(--text-muted)' }}>Subtotal:</span>
                                <span>${cart.total.toFixed(2)}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                <span style={{ color: 'var(--text-muted)' }}>Tax (10%):</span>
                                <span>${(cart.total * 0.1).toFixed(2)}</span>
                            </div>
                            <div
                                style={{
                                    borderTop: '1px solid var(--border-color)',
                                    paddingTop: '0.5rem',
                                    marginTop: '0.5rem',
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.3rem', fontWeight: 700 }}>
                                    <span>Total:</span>
                                    <span style={{ color: 'var(--primary)' }}>
                                        ${(cart.total * 1.1).toFixed(2)}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <button
                            className="btn btn-primary"
                            style={{ width: '100%', marginTop: '1rem' }}
                            onClick={handleCheckout}
                            disabled={checkingOut}
                        >
                            {checkingOut ? 'Processing...' : 'Proceed to Checkout'}
                        </button>

                        {toast && (
                            <div className={`toast ${toast.type}`} style={{ position: 'fixed', bottom: '2rem', right: '2rem' }}>
                                {toast.message}
                            </div>
                        )}

                        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'var(--bg-secondary)', borderRadius: '8px' }}>
                            <div style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem' }}>
                                📊 Data Structure: Doubly Linked List
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                • O(1) add/remove operations<br />
                                • O(1) lookup with hash map<br />
                                • Efficient bidirectional traversal
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Cart;
