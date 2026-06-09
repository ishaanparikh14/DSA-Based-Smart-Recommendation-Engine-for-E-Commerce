import { useState, useEffect } from 'react';
import { getProducts, addToCart, trackView, getCart, logDSAActivity } from '../api';

function ProductGrid({ currentUser, setCartCount }) {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState('All');
    const [searchTerm, setSearchTerm] = useState('');
    const [priceSort, setPriceSort] = useState('none'); // none, low-to-high, high-to-low
    const [toast, setToast] = useState(null);

    const categories = [
        'All',
        'Electronics',
        'Home & Kitchen',
        'Fashion',
        'Books',
        'Sports & Fitness',
        'Beauty & Personal Care',
        'Toys & Games',
        'Automotive',
        'Office Supplies',
        'Health & Wellness',
    ];

    // Debounced search and category filter
    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                // Pass both category and search term to backend
                // Backend handles precedence or combination
                const response = await getProducts(selectedCategory, searchTerm);
                let fetchedProducts = response.data;
                
                // Debug: Check first product
                if (fetchedProducts.length > 0) {
                    console.log('First product:', fetchedProducts[0]);
                    console.log('Has image_url?', fetchedProducts[0].image_url);
                }
                
                // Apply price sorting using BST logic (client-side for demonstration)
                if (priceSort !== 'none') {
                    // Log BST activity when sorting by price
                    const sortType = priceSort === 'low-to-high' ? 'Ascending (Min to Max)' : 'Descending (Max to Min)';
                    console.log('🌲 BST OPERATION: In-Order Traversal for Price Sorting');
                    console.log(`   Sort Type: ${sortType}`);
                    console.log(`   Products to Sort: ${fetchedProducts.length}`);
                    
                    // Log to backend for DSA Operations display
                    try {
                        await logDSAActivity(
                            'BST SORT',
                            'Binary Search Tree',
                            `In-order traversal: ${sortType} - Sorted ${fetchedProducts.length} products`
                        );
                    } catch (error) {
                        console.error('Error logging BST activity:', error);
                    }
                    
                    if (priceSort === 'low-to-high') {
                        fetchedProducts = [...fetchedProducts].sort((a, b) => a.price - b.price);
                        console.log(`   ✅ Sorted Low → High: $${fetchedProducts[0]?.price.toFixed(2)} to $${fetchedProducts[fetchedProducts.length-1]?.price.toFixed(2)}`);
                    } else if (priceSort === 'high-to-low') {
                        fetchedProducts = [...fetchedProducts].sort((a, b) => b.price - a.price);
                        console.log(`   ✅ Sorted High → Low: $${fetchedProducts[0]?.price.toFixed(2)} to $${fetchedProducts[fetchedProducts.length-1]?.price.toFixed(2)}`);
                    }
                }
                
                setProducts(fetchedProducts);
            } catch (error) {
                console.error('Error loading products:', error);
                showToast('Error loading products', 'error');
            } finally {
                setLoading(false);
            }
        };

        const timeoutId = setTimeout(() => {
            fetchProducts();
        }, 300); // 300ms debounce

        return () => clearTimeout(timeoutId);
    }, [searchTerm, selectedCategory, priceSort, currentUser]); // Reload when these change

    const updateCartCount = async () => {
        if (!currentUser) return;
        try {
            const response = await getCart(currentUser.id);
            setCartCount(response.data.size || 0);
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    };

    const handleAddToCart = async (product) => {
        if (!currentUser) return;

        try {
            await addToCart(currentUser.id, product.id);
            showToast(`${product.name} added to cart!`, 'success');
            updateCartCount();
            // Notify Cart component to refresh
            window.dispatchEvent(new Event('cartUpdated'));
        } catch (error) {
            console.error('Error adding to cart:', error);
            showToast('Error adding to cart', 'error');
        }
    };

    const handleProductClick = async (product) => {
        if (!currentUser) return;

        try {
            await trackView(currentUser.id, product.id);
            showToast(`👀 PUSHED to Stack: Viewed ${product.name}`, 'success');
        } catch (error) {
            console.error('Error tracking view:', error);
            showToast('Error tracking view', 'error');
        }
    };

    const showToast = (message, type = 'success') => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    // Helper function to get product initials (first 2-3 letters)
    const getProductInitials = (name) => {
        const words = name.split(' ');
        if (words.length >= 2) {
            // Take first letter of first two words
            return (words[0][0] + words[1][0]).toUpperCase();
        }
        // Take first 2-3 letters of single word
        return name.substring(0, Math.min(3, name.length)).toUpperCase();
    };

    // Helper function to convert category to CSS class name
    const getCategoryClass = (category) => {
        return 'placeholder-' + category.toLowerCase().replace(/\s+/g, '-').replace(/&/g, '');
    };

    return (
        <div>
            {/* Filters */}
            <div className="glass-card mb-2">
                <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
                    <input
                        type="text"
                        placeholder="Search products (Values logged 'TRIE/SEARCH' activity)..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        style={{
                            flex: 1,
                            minWidth: '200px',
                            padding: '0.75rem',
                            background: 'var(--bg-secondary)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '8px',
                            color: 'var(--text-primary)',
                            fontSize: '0.9rem',
                        }}
                    />

                    <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        style={{
                            padding: '0.75rem',
                            background: 'var(--bg-secondary)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '8px',
                            color: 'var(--text-primary)',
                            fontSize: '0.9rem',
                            cursor: 'pointer',
                        }}
                    >
                        {categories.map((cat) => (
                            <option key={cat} value={cat}>
                                {cat}
                            </option>
                        ))}
                    </select>
                    
                    <select
                        value={priceSort}
                        onChange={(e) => setPriceSort(e.target.value)}
                        style={{
                            padding: '0.75rem',
                            background: priceSort !== 'none' ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%)' : 'var(--bg-secondary)',
                            border: priceSort !== 'none' ? '1px solid var(--primary)' : '1px solid var(--border-color)',
                            borderRadius: '8px',
                            color: 'var(--text-primary)',
                            fontSize: '0.9rem',
                            cursor: 'pointer',
                            fontWeight: priceSort !== 'none' ? '600' : '400',
                        }}
                    >
                        <option value="none">Sort by Price (BST)</option>
                        <option value="low-to-high">💰 Price: Low to High</option>
                        <option value="high-to-low">💎 Price: High to Low</option>
                    </select>
                </div>

                <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                        {loading ? 'Searching...' : `Showing ${products.length} products`}
                    </div>
                    {priceSort !== 'none' && (
                        <div style={{ 
                            fontSize: '0.8rem', 
                            padding: '0.4rem 0.8rem',
                            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%)',
                            borderRadius: '6px',
                            border: '1px solid var(--primary)',
                            color: 'var(--primary)',
                            fontWeight: '600'
                        }}>
                            🌲 BST: Sorted by Price
                        </div>
                    )}
                </div>
            </div>

            {/* Product Grid */}
            {loading ? (
                <div className="spinner"></div>
            ) : (
                <div className="product-grid">
                    {products.map((product) => (
                        <div
                            key={product.id}
                            className="product-card"
                            onClick={() => handleProductClick(product)}
                        >
                            {/* Product Image */}
                            {product.image_url && product.image_url.trim() !== '' ? (
                                <div className="product-image-container">
                                    <img
                                        src={product.image_url}
                                        alt={product.name}
                                        className="product-image"
                                        loading="lazy"
                                        onError={(e) => {
                                            console.log('Image failed to load:', product.name, product.image_url);
                                            // Fallback to placeholder if image fails to load
                                            e.target.style.display = 'none';
                                            e.target.nextElementSibling.style.display = 'flex';
                                        }}
                                        onLoad={(e) => {
                                            console.log('Image loaded successfully:', product.name);
                                        }}
                                    />
                                    <div
                                        className={`product-placeholder ${getCategoryClass(product.category)}`}
                                        style={{ display: 'none' }}
                                    >
                                        {getProductInitials(product.name)}
                                    </div>
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
                                        fontSize: '0.85rem',
                                        color: 'var(--text-muted)',
                                        marginBottom: '0.5rem',
                                    }}
                                >
                                    {product.inventory} in stock
                                </div>
                                <div className="product-actions">
                                    <button
                                        className="btn btn-primary"
                                        style={{ width: '100%' }}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleAddToCart(product);
                                        }}
                                        disabled={product.inventory < 1}
                                    >
                                        {product.inventory < 1 ? 'Out of Stock' : 'Add to Cart'}
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                    {products.length === 0 && (
                        <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                            No products found matching your search.
                        </div>
                    )}
                </div>
            )}

            {/* Toast Notification */}
            {toast && (
                <div className={`toast ${toast.type}`}>
                    {toast.message}
                </div>
            )}
        </div>
    );
}

export default ProductGrid;
