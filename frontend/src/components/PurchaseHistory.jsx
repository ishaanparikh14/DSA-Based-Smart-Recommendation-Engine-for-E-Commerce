import { useState, useEffect } from 'react';
import { getUser, getProducts, getCart } from '../api';
import axios from 'axios';

function PurchaseHistory({ currentUser, users, setCurrentUser }) {
    const [purchaseHistory, setPurchaseHistory] = useState([]);
    const [productMap, setProductMap] = useState({});
    const [loading, setLoading] = useState(true);
    const [toast, setToast] = useState(null);

    useEffect(() => {
        loadData();
    }, [currentUser]);

    const loadData = async () => {
        if (!currentUser) return;

        try {
            setLoading(true);

            // Load products
            const productsRes = await getProducts();
            const map = {};
            productsRes.data.forEach((p) => {
                map[p.id] = p;
            });
            setProductMap(map);

            // Load user data
            const userRes = await getUser(currentUser.id);
            setPurchaseHistory(userRes.data.purchase_history || []);
        } catch (error) {
            console.error('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCheckout = async () => {
        try {
            // Get cart items
            const cartRes = await getCart(currentUser.id);
            const cartItems = cartRes.data.items || [];

            if (cartItems.length === 0) {
                showToast('Your cart is empty!', 'error');
                return;
            }

            // Add cart items to purchase history
            const productIds = cartItems.map((item) => item.product_id);

            // Call backend to complete purchase
            const response = await axios.post(
                `http://localhost:5000/api/checkout/${currentUser.id}`,
                { product_ids: productIds }
            );

            if (response.data.success) {
                showToast(`✅ Purchase completed! ${productIds.length} items added to history`, 'success');

                // Dispatch event to notify other components (like graphs) to refresh
                window.dispatchEvent(new CustomEvent('checkoutComplete', { 
                    detail: { userId: currentUser.id, productIds } 
                }));

                // Reload user data
                const updatedUserRes = await getUser(currentUser.id);
                setPurchaseHistory(updatedUserRes.data.purchase_history || []);

                // Update current user in parent
                const updatedUsers = users.map((u) =>
                    u.id === currentUser.id ? updatedUserRes.data : u
                );
                const updatedCurrentUser = updatedUserRes.data;
                setCurrentUser(updatedCurrentUser);

                // Clear cart
                await axios.post(`http://localhost:5000/api/cart/${currentUser.id}/clear`);
            }
        } catch (error) {
            console.error('Error during checkout:', error);
            showToast('Checkout failed. Please try again.', 'error');
        }
    };

    const showToast = (message, type = 'success') => {
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

    if (loading) {
        return <div className="spinner"></div>;
    }

    // Group purchases by product
    const purchaseCounts = {};
    purchaseHistory.forEach((productId) => {
        purchaseCounts[productId] = (purchaseCounts[productId] || 0) + 1;
    });

    const uniqueProducts = Object.keys(purchaseCounts).map((id) => parseInt(id));

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Purchase History</h1>
                <button
                    className="btn btn-primary"
                    onClick={handleCheckout}
                >
                    🛒 Checkout Cart
                </button>
            </div>

            {purchaseHistory.length === 0 ? (
                <div className="glass-card text-center" style={{ padding: '3rem' }}>
                    <h2>No purchase history yet</h2>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
                        Start shopping and checkout to build your purchase history!
                    </p>
                </div>
            ) : (
                <>
                    <div className="glass-card mb-2">
                        <h3 style={{ marginBottom: '1rem' }}>
                            Total Purchases: {purchaseHistory.length} items ({uniqueProducts.length} unique products)
                        </h3>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                            Your purchase history influences personalized recommendations
                        </p>
                    </div>

                    <div className="product-grid">
                        {uniqueProducts.map((productId) => {
                            const product = productMap[productId];
                            const count = purchaseCounts[productId];

                            if (!product) return null;

                            return (
                                <div key={productId} className="product-card">
                                    {product.image_url ? (
                                        <div style={{
                                            width: '100%',
                                            height: '200px',
                                            overflow: 'hidden',
                                            background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                        }}>
                                            <img
                                                src={product.image_url}
                                                alt={product.name}
                                                style={{
                                                    width: '100%',
                                                    height: '100%',
                                                    objectFit: 'contain',
                                                    padding: '10px',
                                                }}
                                                onError={(e) => {
                                                    e.target.style.display = 'none';
                                                    const placeholder = document.createElement('div');
                                                    placeholder.className = `product-placeholder ${getCategoryClass(product.category)}`;
                                                    placeholder.style.cssText = 'width: 100%; height: 200px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;';
                                                    placeholder.textContent = getProductInitials(product.name);
                                                    e.target.parentElement.replaceWith(placeholder);
                                                }}
                                            />
                                        </div>
                                    ) : (
                                        <div
                                            className={`product-placeholder ${getCategoryClass(product.category)}`}
                                        >
                                            {getProductInitials(product.name)}
                                        </div>
                                    )}
                                    <div className="product-info">
                                        <div className="product-category">{product.category}</div>
                                        <div className="product-name">{product.name}</div>
                                        <div className="product-price">${product.price.toFixed(2)}</div>
                                        <div
                                            style={{
                                                marginTop: '0.5rem',
                                                padding: '0.5rem',
                                                background: 'var(--bg-secondary)',
                                                borderRadius: '8px',
                                                textAlign: 'center',
                                            }}
                                        >
                                            <strong>Purchased {count} time{count > 1 ? 's' : ''}</strong>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </>
            )}

            {/* Checkout Info */}
            <div className="glass-card mt-3">
                <h3 style={{ marginBottom: '1rem' }}>💡 How Checkout Works</h3>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                    <p style={{ marginBottom: '0.5rem' }}>
                        1. Add products to your cart
                    </p>
                    <p style={{ marginBottom: '0.5rem' }}>
                        2. Click "Checkout Cart" button above
                    </p>
                    <p style={{ marginBottom: '0.5rem' }}>
                        3. Cart items are added to your purchase history
                    </p>
                    <p style={{ marginBottom: '0.5rem' }}>
                        4. Your preferred categories are updated
                    </p>
                    <p>
                        5. Recommendations will change based on your new purchase history!
                    </p>
                </div>
            </div>

            {/* Toast */}
            {toast && (
                <div className={`toast ${toast.type}`}>
                    {toast.message}
                </div>
            )}
        </div>
    );
}

export default PurchaseHistory;
