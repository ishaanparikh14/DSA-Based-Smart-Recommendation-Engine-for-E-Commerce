import { useState, useEffect } from 'react';
import { getDSAActivity, getRecommendations, getCart, getRecentViews, getSessionQueue } from '../api';

function DSAApplications({ currentUser }) {
    const [activities, setActivities] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [recExplanation, setRecExplanation] = useState(null);
    const [cart, setCart] = useState(null);
    const [recentViews, setRecentViews] = useState([]);
    const [sessionQueue, setSessionQueue] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!currentUser) return;

        const loadData = async () => {
            try {
                setLoading(true);

                // Load DSA activity
                const activityRes = await getDSAActivity(20);
                setActivities(activityRes.data.reverse());

                // Load recommendations with explanation
                const recRes = await getRecommendations(currentUser.id, 10, true);
                setRecommendations(recRes.data.recommendations || []);
                setRecExplanation(recRes.data.explanation);

                // Load cart
                const cartRes = await getCart(currentUser.id);
                setCart(cartRes.data);

                // Load recent views
                const viewsRes = await getRecentViews(currentUser.id);
                setRecentViews(viewsRes.data || []);

                // Load session queue
                const queueRes = await getSessionQueue(currentUser.id);
                setSessionQueue(queueRes.data.queue || []);

            } catch (error) {
                console.error('Error loading DSA data:', error);
            } finally {
                setLoading(false);
            }
        };

        loadData();

        // Auto-refresh every 3 seconds
        const interval = setInterval(async () => {
            try {
                const activityRes = await getDSAActivity(20);
                setActivities(activityRes.data.reverse());

                // Also refresh stats that might change with interaction
                if (currentUser) {
                    const queueRes = await getSessionQueue(currentUser.id);
                    setSessionQueue(queueRes.data.queue || []);
                    const viewsRes = await getRecentViews(currentUser.id);
                    setRecentViews(viewsRes.data || []);
                    const cartRes = await getCart(currentUser.id);
                    setCart(cartRes.data);
                }
            } catch (error) {
                console.error('Error refreshing activity:', error);
            }
        }, 3000);

        return () => clearInterval(interval);
    }, [currentUser]);

    if (!currentUser) {
        return (
            <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
                <h2>Please select a user to view DSA Applications</h2>
            </div>
        );
    }

    if (loading) {
        return <div className="spinner"></div>;
    }

    return (
        <div className="dsa-applications">
            <div className="dsa-header">
                <h1>🧠 DSA Applications in Action</h1>
                <p className="subtitle">Data Structures & Algorithms powering this E-Commerce Engine</p>
            </div>

            {/* Data Structures Table */}
            <section className="dsa-section">
                <div className="section-header">
                    <h2>📊 Data Structures Used</h2>
                </div>
                <div className="glass-card" style={{ padding: '0', overflow: 'hidden' }}>
                    <table style={{ 
                        width: '100%', 
                        borderCollapse: 'collapse',
                        fontSize: '0.95rem'
                    }}>
                        <thead style={{ 
                            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15))',
                            borderBottom: '2px solid rgba(99, 102, 241, 0.3)'
                        }}>
                            <tr>
                                <th style={{ padding: '1rem', textAlign: 'left', fontWeight: 700, color: '#818cf8' }}>Data Structure</th>
                                <th style={{ padding: '1rem', textAlign: 'left', fontWeight: 700, color: '#818cf8' }}>Application</th>
                                <th style={{ padding: '1rem', textAlign: 'left', fontWeight: 700, color: '#818cf8' }}>Operations</th>
                                <th style={{ padding: '1rem', textAlign: 'left', fontWeight: 700, color: '#818cf8' }}>Time Complexity</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🕸️ <span>Graph (Weighted)</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Co-occurrence tracking for frequently bought together recommendations
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    BFS/DFS traversal, neighbor queries
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(V + E)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🔎 <span>Trie</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Autocomplete search, category filtering by prefix
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Prefix search, insertion, starts_with queries
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(m)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🌳 <span>Binary Search Tree</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Price-based product filtering and range queries
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Search, insert, range queries
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(log n)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🔥 <span>Min Heap</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Top-K recommendation selection based on scores
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Extract-min, heapify, insert
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(log n)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🔗 <span>Doubly Linked List</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Shopping cart management with O(1) add/remove
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Insert, delete, traversal
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(1)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        📚 <span>Stack (LIFO)</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Recently viewed products (browsing history)
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Push, pop, peek
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(1)</code>
                                </td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        ⏭️ <span>Queue (FIFO)</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    User session activity tracking and action ordering
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Enqueue, dequeue, peek
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(1)</code>
                                </td>
                            </tr>
                            <tr>
                                <td style={{ padding: '1rem', fontWeight: 600, color: '#c4b5fd' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        🗂️ <span>Hash Map</span>
                                    </div>
                                </td>
                                <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                                    Fast product lookups, user data caching, cart item access
                                </td>
                                <td style={{ padding: '1rem', color: '#94a3b8' }}>
                                    Get, set, delete, has
                                </td>
                                <td style={{ padding: '1rem' }}>
                                    <code style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '0.25rem 0.5rem', borderRadius: '4px', color: '#fbbf24' }}>O(1) avg</code>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            {/* Recommendation Pipeline - DETAILED */}
            <section className="dsa-section pipeline-section">
                <div className="section-header">
                    <h2>🎯 Recommendation Pipeline (6-Stage Process)</h2>
                    <p>Category-First Approach using Graph → Trie → BST → Heap</p>
                </div>

                {recExplanation && (
                    <div className="pipeline-visualization">
                        {/* Stage 1: Co-occurrence Graph */}
                        <div className="pipeline-stage">
                            <div className="stage-number">1</div>
                            <div className="stage-content">
                                <h3>🕸️ Co-occurrence Graph</h3>
                                <div className="stage-ds">Data Structure: <strong>Weighted Graph</strong></div>
                                <div className="stage-desc">
                                    Finds products frequently bought together based on transaction history
                                </div>
                                <div className="stage-data">
                                    <div className="data-label">Graph Edges Traversed:</div>
                                    <div className="data-value">{recExplanation.co_occurrence_candidates?.length || 0}</div>
                                </div>
                                {recExplanation.co_occurrence_candidates && recExplanation.co_occurrence_candidates.length > 0 && (
                                    <div className="candidates-list">
                                        {recExplanation.co_occurrence_candidates.slice(0, 5).map((c, i) => (
                                            <div key={i} className="candidate-item">
                                                Product #{c.product_id} (Score: {c.score.toFixed(2)})
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="pipeline-arrow">→</div>

                        {/* Stage 2: Collaborative Filtering */}
                        <div className="pipeline-stage">
                            <div className="stage-number">2</div>
                            <div className="stage-content">
                                <h3>👥 Collaborative Filtering</h3>
                                <div className="stage-ds">Algorithm: <strong>Jaccard Similarity</strong></div>
                                <div className="stage-desc">
                                    Finds similar users using Set operations (Intersection ÷ Union)
                                </div>
                                <div className="stage-data">
                                    <div className="data-label">Similar Users Found:</div>
                                    <div className="data-value">{recExplanation.collaborative_candidates?.length || 0}</div>
                                </div>
                            </div>
                        </div>

                        <div className="pipeline-arrow">→</div>

                        {/* Stage 3: Category Filter (Trie) */}
                        <div className="pipeline-stage critical">
                            <div className="stage-number">3</div>
                            <div className="stage-content">
                                <h3>🌳 Category Filter</h3>
                                <div className="stage-ds">Data Structure: <strong>Trie (Prefix Tree)</strong></div>
                                <div className="stage-desc">
                                    <strong>CRITICAL:</strong> Ensures recommendations match user's preferred categories
                                </div>
                                <div className="stage-data">
                                    <div className="data-label">User Preferred Categories:</div>
                                    <div className="data-value">
                                        {currentUser.preferred_categories?.join(', ') || 'All'}
                                    </div>
                                </div>
                                <div className="trie-visualization" style={{ marginTop: '0.5rem', fontSize: '0.8rem', opacity: 0.8 }}>
                                    Matching Prefix: <strong>{currentUser.preferred_categories && currentUser.preferred_categories.length > 0 ? currentUser.preferred_categories[0].substring(0, 4) + '...' : 'ROOT'}</strong>
                                </div>
                            </div>
                        </div>

                        <div className="pipeline-arrow">→</div>

                        {/* Stage 4: BST Ranking */}
                        <div className="pipeline-stage">
                            <div className="stage-number">4</div>
                            <div className="stage-content">
                                <h3>🔍 Price & Inventory Filter</h3>
                                <div className="stage-ds">Data Structure: <strong>Binary Search Tree</strong></div>
                                <div className="stage-desc">
                                    Filters by price range and inventory availability
                                </div>
                                <div className="stage-data">
                                    <div className="data-label">After BST Filter:</div>
                                    <div className="data-value">{recExplanation.after_ranking || 0} products</div>
                                </div>
                            </div>
                        </div>

                        <div className="pipeline-arrow">→</div>

                        {/* Stage 5: Top-K Selection (Heap) */}
                        <div className="pipeline-stage">
                            <div className="stage-number">5</div>
                            <div className="stage-content">
                                <h3>🏆 Top-K Selection</h3>
                                <div className="stage-ds">Data Structure: <strong>Min-Heap</strong></div>
                                <div className="stage-desc">
                                    Efficiently selects top 10 recommendations in O(n log k) time
                                </div>
                                <div className="stage-data">
                                    <div className="data-label">Final Recommendations:</div>
                                    <div className="data-value">{recommendations.length}</div>
                                </div>
                            </div>
                        </div>

                        <div className="pipeline-arrow">→</div>

                        {/* Stage 6: Results */}
                        <div className="pipeline-stage results">
                            <div className="stage-number">✓</div>
                            <div className="stage-content">
                                <h3>✨ Final Results</h3>
                                <div className="recommendations-preview">
                                    {recommendations.slice(0, 3).map((rec, i) => (
                                        <div key={i} className="rec-item">
                                            <div className="rec-name">{rec.name}</div>
                                            <div className="rec-score">Score: {rec.score?.toFixed(2) || 'N/A'}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </section>

            {/* Other Data Structures */}
            <section className="dsa-section">
                <h2>📚 Other Data Structures in Use</h2>
                <div className="ds-grid">
                    {/* Shopping Cart - Doubly Linked List */}
                    <div className="ds-card">
                        <div className="ds-icon">🛒</div>
                        <h3>Shopping Cart</h3>
                        <div className="ds-name">Doubly Linked List</div>
                        <div className="ds-stats">
                            <div className="stat">
                                <span className="stat-label">Items:</span>
                                <span className="stat-value">{cart?.size || 0}</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Operations:</span>
                                <span className="stat-value">O(1) Insert/Delete</span>
                            </div>
                        </div>
                        <div className="ds-desc">
                            Allows efficient addition and removal from both ends. Each cart item points to next and previous items.
                        </div>
                    </div>

                    {/* Recent Views - Stack */}
                    <div className="ds-card">
                        <div className="ds-icon">📜</div>
                        <h3>Recent Views</h3>
                        <div className="ds-name">Stack (LIFO)</div>
                        <div className="ds-stats">
                            <div className="stat">
                                <span className="stat-label">Views:</span>
                                <span className="stat-value">{recentViews.length}</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Operations:</span>
                                <span className="stat-value">O(1) Push/Pop</span>
                            </div>
                        </div>
                        <div className="ds-desc">
                            Last-In-First-Out structure tracks browsing history. Most recent view is always on top.
                        </div>

                        <button
                            className="btn btn-secondary"
                            style={{
                                width: '100%',
                                marginTop: '1rem',
                                marginBottom: '1rem',
                                border: '1px solid var(--primary)',
                                color: 'var(--primary)'
                            }}
                            onClick={async () => {
                                if (!recentViews || recentViews.length === 0) return;
                                try {
                                    // Pop from backend
                                    // We need to import popView in DSAApplications.jsx first
                                    // For now, let's assume it's imported or will be
                                    const { popView } = await import('../api');
                                    await popView(currentUser.id);

                                    // Refresh view
                                    const { getRecentViews, getDSAActivity } = await import('../api');
                                    const viewsRes = await getRecentViews(currentUser.id);
                                    setRecentViews(viewsRes.data.views || []);

                                    // Show toast/activity
                                    const activityRes = await getDSAActivity(20);
                                    setActivities(activityRes.data.reverse());
                                } catch (err) {
                                    console.error("Error popping view:", err);
                                }
                            }}
                            disabled={recentViews.length === 0}
                        >
                            ↩️ POP (Undo View)
                        </button>

                        {recentViews && recentViews.length > 0 && (
                            <div className="stack-visualizer">
                                <div className="stack-label">Stack Top (Most Recent)</div>
                                {recentViews.slice(0, 5).map((view, idx) => (
                                    <div key={idx} className="stack-item">
                                        <span className="stack-index">{idx + 1}.</span>
                                        <span className="stack-product">
                                            {view.product ? view.product.name : `Product #${view.product_id}`}
                                        </span>
                                    </div>
                                ))}
                                {recentViews.length > 5 && (
                                    <div className="stack-more">... and {recentViews.length - 5} more</div>
                                )}
                            </div>
                        )}
                        {recentViews.length === 0 && (
                            <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '1rem', fontSize: '0.9rem' }}>
                                Stack is empty. View products to Push!
                            </div>
                        )}
                    </div>

                    {/* Product Catalog - Hash Map */}
                    <div className="ds-card">
                        <div className="ds-icon">🗂️</div>
                        <h3>Product Catalog</h3>
                        <div className="ds-name">Hash Map</div>
                        <div className="ds-stats">
                            <div className="stat">
                                <span className="stat-label">Products:</span>
                                <span className="stat-value">89</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Lookup:</span>
                                <span className="stat-value">O(1) Average</span>
                            </div>
                        </div>
                        <div className="ds-desc">
                            Instant product lookup by ID using hash function. Handles collisions with chaining.
                        </div>
                    </div>

                    {/* Session Queue */}
                    <div className="ds-card">
                        <div className="ds-icon">⏱️</div>
                        <h3>Session Tracking</h3>
                        <div className="ds-name">Queue (FIFO)</div>
                        <div className="ds-stats">
                            <div className="stat">
                                <span className="stat-label">Operations:</span>
                                <span className="stat-value">O(1) Enqueue</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Items:</span>
                                <span className="stat-value">{sessionQueue.length}</span>
                            </div>
                        </div>
                        <div className="ds-desc">
                            First-In-First-Out structure tracks user actions. New actions add to rear, old processed from front.
                        </div>

                        <button
                            className="btn btn-secondary"
                            style={{
                                width: '100%',
                                marginTop: '1rem',
                                marginBottom: '1rem',
                                border: '1px solid var(--accent)',
                                color: 'var(--accent)'
                            }}
                            onClick={async () => {
                                if (!sessionQueue || sessionQueue.length === 0) return;
                                try {
                                    // Dequeue from backend
                                    const { dequeueSessionItem } = await import('../api');
                                    await dequeueSessionItem(currentUser.id);

                                    // Refresh view
                                    const { getSessionQueue, getDSAActivity } = await import('../api');
                                    const queueRes = await getSessionQueue(currentUser.id);
                                    setSessionQueue(queueRes.data.queue || []);

                                    // Show toast/activity
                                    const activityRes = await getDSAActivity(20);
                                    setActivities(activityRes.data.reverse());
                                } catch (err) {
                                    console.error("Error dequeuing item:", err);
                                }
                            }}
                            disabled={sessionQueue.length === 0}
                        >
                            📤 DEQUEUE (Process Item)
                        </button>
                        {sessionQueue && sessionQueue.length > 0 && (
                            <div className="stack-visualizer" style={{ marginTop: '1rem' }}>
                                <div className="stack-label">Queue Front (Oldest)</div>
                                {sessionQueue.slice(0, 5).map((item, idx) => (
                                    <div key={idx} className="stack-item">
                                        <span className="stack-index">{idx + 1}.</span>
                                        <span className="stack-product" style={{ fontSize: '0.8rem' }}>
                                            {item.action === 'view_product' && '👀 Viewed Product'}
                                            {item.action === 'add_to_cart' && '🛒 Added to Cart'}
                                            {item.product_id && ` #${item.product_id}`}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}

export default DSAApplications;
