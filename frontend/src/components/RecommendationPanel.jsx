import { useState, useEffect } from 'react';
import { getRecommendations, explainRecommendation, addToCart, getCart } from '../api';

function RecommendationPanel({ currentUser, setCartCount }) {
    const [recommendations, setRecommendations] = useState([]);
    const [explanation, setExplanation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [toast, setToast] = useState(null);

    useEffect(() => {
        loadRecommendations();
    }, [currentUser]);

    const loadRecommendations = async () => {
        if (!currentUser) return;

        try {
            setLoading(true);
            const response = await getRecommendations(currentUser.id, 10, true);
            setRecommendations(response.data.recommendations);
            setExplanation(response.data.explanation);
        } catch (error) {
            console.error('Error loading recommendations:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleExplain = async (productId) => {
        try {
            const response = await explainRecommendation(currentUser.id, productId);
            setSelectedProduct(response.data);
        } catch (error) {
            console.error('Error explaining recommendation:', error);
        }
    };

    const handleAddToCart = async (product) => {
        try {
            await addToCart(currentUser.id, product.product_id);
            showToast(`${product.product.name} added to cart!`, 'success');
            updateCartCount();
        } catch (error) {
            console.error('Error adding to cart:', error);
            showToast('Error adding to cart', 'error');
        }
    };

    const updateCartCount = async () => {
        try {
            const response = await getCart(currentUser.id);
            setCartCount(response.data.size || 0);
        } catch (error) {
            console.error('Error updating cart count:', error);
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

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Personalized Recommendations</h1>
                <button
                    className="btn btn-primary"
                    onClick={loadRecommendations}
                    disabled={loading}
                >
                    🔄 {loading ? 'Loading...' : 'Refresh'}
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 3fr) 350px', gap: '2rem', alignItems: 'start' }}>

                {/* Main Content: Recommendations Grid */}
                <div>
                    {recommendations.length > 0 ? (
                        <div className="product-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))' }}>
                            {recommendations.map((rec) => {
                                const product = rec.product;
                                if (!product) return null;

                                return (
                                    <div key={product.id} className="product-card" style={{ position: 'relative' }}>
                                        <div
                                            style={{
                                                position: 'absolute',
                                                top: '10px',
                                                right: '10px',
                                                background: rec.score > 100 ? 'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                                color: 'white',
                                                padding: '0.4rem 0.8rem',
                                                borderRadius: '12px',
                                                fontSize: '0.75rem',
                                                fontWeight: 700,
                                                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
                                                zIndex: 10,
                                                display: 'flex',
                                                flexDirection: 'column',
                                                alignItems: 'center',
                                                gap: '2px'
                                            }}
                                        >
                                            <div style={{ fontSize: '0.85rem' }}>
                                                {rec.score > 100 ? '🔥 Cart' : '⭐'}
                                            </div>
                                            <div style={{ fontSize: '0.7rem', opacity: 0.95 }}>
                                                Score: {rec.score.toFixed(1)}
                                            </div>
                                        </div>

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
                                                        placeholder.style.cssText = 'width: 100%; height: 200px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; color: rgba(255, 255, 255, 0.95);';
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

                                            <div className="product-actions" style={{ flexDirection: 'column' }}>
                                                <button
                                                    className="btn btn-primary"
                                                    style={{ width: '100%' }}
                                                    onClick={() => handleAddToCart(rec)}
                                                    disabled={product.inventory < 1}
                                                >
                                                    {product.inventory < 1 ? 'Out of Stock' : 'Add to Cart'}
                                                </button>
                                                <button
                                                    className="btn btn-secondary"
                                                    style={{ width: '100%', marginTop: '0.5rem' }}
                                                    onClick={() => handleExplain(product.id)}
                                                >
                                                    Why recommended?
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="glass-card text-center" style={{ padding: '3rem' }}>
                            <h3>No recommendations available</h3>
                            <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
                                Start browsing products to get personalized recommendations!
                            </p>
                        </div>
                    )}
                </div>

                {/* Sidebar: Algorithm Explanation */}
                <div style={{ position: 'sticky', top: '100px' }}>
                    {explanation && (
                        <div className="glass-card">
                            <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
                                🧠 How It Works
                            </h3>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                                6-Stage Category-First Pipeline
                            </div>
                            
                            <div style={{ 
                                padding: '0.75rem', 
                                background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%)',
                                borderRadius: '8px',
                                border: '1px solid rgba(99, 102, 241, 0.2)',
                                marginBottom: '1rem',
                                fontSize: '0.75rem'
                            }}>
                                <strong>📊 Scoring Algorithm:</strong>
                                <div style={{ marginTop: '0.5rem', lineHeight: '1.6' }}>
                                    <div>• Category Match: +40 points</div>
                                    <div>• Purchase History: +30 points</div>
                                    <div>• View History: +20 points</div>
                                    <div>• Popularity: +10 points</div>
                                    <div>• Cart Boost: +100 points 🔥</div>
                                </div>
                            </div>

                            <div style={{ display: 'grid', gap: '0.5rem' }}>
                                {explanation.stages.map((stage) => (
                                    <div
                                        key={stage.stage}
                                        style={{
                                            padding: '0.75rem',
                                            background: 'var(--bg-secondary)',
                                            borderRadius: '8px',
                                            borderLeft: `3px solid ${stage.name.includes('Cart') ? '#ec4899' : 'var(--primary)'}`,
                                        }}
                                    >
                                        <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.25rem' }}>
                                            {stage.stage === 2.5 ? '⚡ ' : ''}{stage.name}
                                        </div>
                                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                            {stage.candidates !== undefined && `${stage.candidates} candidates`}
                                            {stage.removed > 0 && ` • Removed ${stage.removed}`}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {explanation.user_categories && (
                                <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
                                    <strong style={{ fontSize: '0.85rem' }}>Your Interests:</strong>
                                    <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.25rem', flexWrap: 'wrap' }}>
                                        {explanation.stages[3]?.user_categories?.slice(0, 5).map((cat) => (
                                            <span
                                                key={cat}
                                                style={{
                                                    padding: '0.2rem 0.5rem',
                                                    background: 'var(--bg-tertiary)',
                                                    borderRadius: '4px',
                                                    fontSize: '0.7rem',
                                                    color: 'var(--text-secondary)'
                                                }}
                                            >
                                                {cat}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Explanation Modal (Same as before) */}
            {selectedProduct && (
                <div className="modal-overlay" onClick={() => setSelectedProduct(null)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <h2 style={{ marginBottom: '1rem' }}>
                            Why we recommended: {selectedProduct.product_name}
                        </h2>

                        <div style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
                            Category: {selectedProduct.product_category}
                        </div>

                        <div style={{ display: 'grid', gap: '1rem' }}>
                            {selectedProduct.reasons?.map((reason, index) => (
                                <div
                                    key={index}
                                    style={{
                                        padding: '1rem',
                                        background: 'var(--bg-tertiary)',
                                        borderRadius: '8px',
                                        borderLeft: '3px solid var(--primary)',
                                    }}
                                >
                                    <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>
                                        {reason.type.replace(/_/g, ' ').toUpperCase()}
                                    </div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                        {reason.description}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                        Score: {reason.score.toFixed(2)}
                                    </div>
                                </div>
                            ))}

                            {(!selectedProduct.reasons || selectedProduct.reasons.length === 0) && (
                                <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>
                                    No specific reasons available
                                </div>
                            )}
                        </div>

                        <button
                            className="btn btn-secondary"
                            style={{ width: '100%', marginTop: '1.5rem' }}
                            onClick={() => setSelectedProduct(null)}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}

            {/* Toast */}
            {toast && (
                <div className={`toast ${toast.type}`}>
                    {toast.message}
                </div>
            )}
        </div>
    );
}

export default RecommendationPanel;
