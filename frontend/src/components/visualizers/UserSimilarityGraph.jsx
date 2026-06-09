import { useState, useEffect, useCallback } from 'react';
import { getUserSimilarityGraph, getUserOrderHistory } from '../../api';

/**
 * UserSimilarityGraph - Complete graph showing all users connected with 
 * Jaccard similarity scores as edge weights.
 * 
 * Clicking on a user node shows their order history as disjoint graphs.
 */
function UserSimilarityGraph() {
    const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
    const [loading, setLoading] = useState(true);
    const [selectedUser, setSelectedUser] = useState(null);
    const [orderData, setOrderData] = useState(null);
    const [hoveredNode, setHoveredNode] = useState(null);
    const [hoveredEdge, setHoveredEdge] = useState(null);
    const [refreshing, setRefreshing] = useState(false);

    const width = 700;
    const height = 500;
    const orderWidth = 900;
    const orderHeight = 400;

    // Fetch user similarity graph
    const fetchSimilarityGraph = useCallback(async (isRefresh = false) => {
        try {
            if (isRefresh) {
                setRefreshing(true);
            } else {
                setLoading(true);
            }
            const response = await getUserSimilarityGraph();
            setGraphData(response.data);
        } catch (error) {
            console.error('Error fetching similarity graph:', error);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }, []);

    // Fetch order history for selected user
    const fetchOrderHistory = useCallback(async (userId) => {
        try {
            const response = await getUserOrderHistory(userId);
            setOrderData(response.data);
        } catch (error) {
            console.error('Error fetching order history:', error);
        }
    }, []);

    useEffect(() => {
        fetchSimilarityGraph();
        
        // Listen for checkout events to refresh the graph
        const handleCheckoutComplete = () => {
            console.log('Checkout detected - refreshing User Similarity Graph');
            setTimeout(() => {
                fetchSimilarityGraph(true); // Pass true to indicate this is a refresh
                // Also refresh order data if a user is selected
                if (selectedUser) {
                    fetchOrderHistory(selectedUser.id);
                }
            }, 1000); // Small delay to allow backend to process
        };
        
        window.addEventListener('checkoutComplete', handleCheckoutComplete);
        
        return () => {
            window.removeEventListener('checkoutComplete', handleCheckoutComplete);
        };
    }, [fetchSimilarityGraph, selectedUser, fetchOrderHistory]);

    useEffect(() => {
        if (selectedUser) {
            fetchOrderHistory(selectedUser.id);
        } else {
            setOrderData(null);
        }
    }, [selectedUser, fetchOrderHistory]);

    // Calculate positions for users in a circle (complete graph layout)
    const calculateUserPositions = useCallback(() => {
        const { nodes } = graphData;
        if (nodes.length === 0) return [];

        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.35;

        return nodes.map((node, index) => {
            const angle = (2 * Math.PI * index) / nodes.length - Math.PI / 2;
            return {
                ...node,
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle),
                radius: 22 + (node.purchase_count || 0) * 1, // Size based on purchases (smaller)
            };
        });
    }, [graphData, width, height]);

    // Calculate positions for order products (disjoint clusters)
    const calculateOrderPositions = useCallback(() => {
        if (!orderData || !orderData.nodes || orderData.nodes.length === 0) return [];

        const orders = orderData.orders || [];
        const clusterWidth = orderWidth / (orders.length + 1);

        const positioned = [];

        orders.forEach((order, orderIdx) => {
            const orderNodes = orderData.nodes.filter(n => n.order_id === order.order_id);
            const clusterCenterX = clusterWidth * (orderIdx + 1);
            const clusterCenterY = orderHeight / 2;
            const nodeRadius = 120 / Math.max(orderNodes.length, 1);

            orderNodes.forEach((node, nodeIdx) => {
                const angle = (2 * Math.PI * nodeIdx) / orderNodes.length - Math.PI / 2;
                const r = orderNodes.length === 1 ? 0 : 50;
                positioned.push({
                    ...node,
                    x: clusterCenterX + r * Math.cos(angle),
                    y: clusterCenterY + r * Math.sin(angle),
                    radius: 28,
                });
            });
        });

        return positioned;
    }, [orderData, orderWidth, orderHeight]);

    const positionedUsers = calculateUserPositions();
    const positionedOrders = calculateOrderPositions();

    // Get user position by ID
    const getUserPosition = (userId) => {
        const user = positionedUsers.find(u => u.id === userId);
        return user ? { x: user.x, y: user.y } : { x: 0, y: 0 };
    };

    // Get order node position by ID
    const getOrderNodePosition = (nodeId) => {
        const node = positionedOrders.find(n => n.id === nodeId);
        return node ? { x: node.x, y: node.y } : { x: 0, y: 0 };
    };

    // Get edge color based on similarity weight
    const getEdgeColor = (weight, isHighlighted) => {
        if (weight >= 0.5) return isHighlighted ? '#10b981' : 'rgba(16, 185, 129, 0.6)';
        if (weight >= 0.3) return isHighlighted ? '#3b82f6' : 'rgba(59, 130, 246, 0.5)';
        if (weight >= 0.1) return isHighlighted ? '#f59e0b' : 'rgba(245, 158, 11, 0.4)';
        return isHighlighted ? '#6b7280' : 'rgba(107, 114, 128, 0.2)';
    };

    // Get edge width based on weight
    const getEdgeWidth = (weight, isHighlighted) => {
        const base = 1 + weight * 6;
        return isHighlighted ? base + 2 : base;
    };

    // Get initials
    const getInitials = (name) => {
        if (!name) return '?';
        const words = name.split(' ');
        if (words.length >= 2) {
            return (words[0][0] + words[1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    };

    if (loading) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <div className="spinner" style={{ margin: '0 auto' }}></div>
                <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>
                    Loading user similarity graph...
                </p>
            </div>
        );
    }

    return (
        <div style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div>
                    <h2 style={{ margin: 0 }}>👥 User Similarity Graph (Complete Graph)</h2>
                    <p style={{ color: 'var(--text-muted)', margin: '0.5rem 0 0', fontSize: '0.9rem' }}>
                        All users connected with <strong>Jaccard Similarity</strong> scores as edge weights.
                        <strong style={{ color: '#f59e0b' }}> Click on a user node</strong> to see their order history.
                    </p>
                </div>
                {refreshing && (
                    <div style={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: '0.5rem',
                        padding: '0.5rem 1rem',
                        background: 'rgba(59, 130, 246, 0.1)',
                        border: '1px solid #3b82f6',
                        borderRadius: '8px',
                        color: '#3b82f6',
                        fontSize: '0.9rem',
                        fontWeight: '600'
                    }}>
                        <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                        Updating after purchase...
                    </div>
                )}
            </div>

            {/* Legend */}
            <div style={{
                display: 'flex',
                gap: '1.5rem',
                marginBottom: '1rem',
                fontSize: '0.8rem',
                color: 'var(--text-secondary)',
                flexWrap: 'wrap',
                padding: '0.75rem 1rem',
                background: 'var(--bg-secondary)',
                borderRadius: '8px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '30px', height: '3px', background: '#10b981' }}></div>
                    <span>High (≥0.5)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '30px', height: '3px', background: '#3b82f6' }}></div>
                    <span>Medium (≥0.3)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '30px', height: '3px', background: '#f59e0b' }}></div>
                    <span>Low (≥0.1)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '30px', height: '1px', background: '#6b7280' }}></div>
                    <span>Very Low (&lt;0.1)</span>
                </div>
            </div>

            {/* Main User Similarity Graph */}
            <div style={{
                background: 'linear-gradient(180deg, #0f172a 0%, #1e293b 100%)',
                borderRadius: '12px',
                border: '1px solid var(--border-color)',
                padding: '1rem',
                marginBottom: '1.5rem'
            }}>
                <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`}>
                    <defs>
                        <linearGradient id="userNodeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#f59e0b" />
                            <stop offset="100%" stopColor="#d97706" />
                        </linearGradient>
                        <linearGradient id="selectedUserGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#ec4899" />
                            <stop offset="100%" stopColor="#be185d" />
                        </linearGradient>
                        <filter id="userGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="4" result="coloredBlur" />
                            <feMerge>
                                <feMergeNode in="coloredBlur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    {/* Edges - All users connected */}
                    <g className="edges">
                        {graphData.edges.map((edge, index) => {
                            const source = getUserPosition(edge.source);
                            const target = getUserPosition(edge.target);
                            const isHighlighted = hoveredEdge === index ||
                                hoveredNode === edge.source || hoveredNode === edge.target;

                            return (
                                <g key={`edge-${index}`}
                                    onMouseEnter={() => setHoveredEdge(index)}
                                    onMouseLeave={() => setHoveredEdge(null)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <line
                                        x1={source.x}
                                        y1={source.y}
                                        x2={target.x}
                                        y2={target.y}
                                        stroke={getEdgeColor(edge.weight, isHighlighted)}
                                        strokeWidth={getEdgeWidth(edge.weight, isHighlighted)}
                                        strokeLinecap="round"
                                        style={{ transition: 'all 0.3s ease' }}
                                    />
                                    {/* Weight label on hover */}
                                    {isHighlighted && edge.weight > 0 && (
                                        <text
                                            x={(source.x + target.x) / 2}
                                            y={(source.y + target.y) / 2}
                                            textAnchor="middle"
                                            fill="#fff"
                                            fontSize="12px"
                                            fontWeight="bold"
                                            style={{
                                                background: 'black',
                                                pointerEvents: 'none'
                                            }}
                                        >
                                            {(edge.weight * 100).toFixed(0)}%
                                        </text>
                                    )}
                                </g>
                            );
                        })}
                    </g>

                    {/* User Nodes */}
                    <g className="nodes">
                        {positionedUsers.map((user, index) => {
                            const isHovered = hoveredNode === user.id;
                            const isSelected = selectedUser?.id === user.id;

                            return (
                                <g
                                    key={user.id}
                                    transform={`translate(${user.x}, ${user.y})`}
                                    onMouseEnter={() => setHoveredNode(user.id)}
                                    onMouseLeave={() => setHoveredNode(null)}
                                    onClick={() => setSelectedUser(isSelected ? null : user)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    {/* Node circle */}
                                    <circle
                                        r={isHovered || isSelected ? user.radius + 5 : user.radius}
                                        fill={isSelected ? 'url(#selectedUserGradient)' : 'url(#userNodeGradient)'}
                                        stroke={isSelected ? '#f472b6' : '#fbbf24'}
                                        strokeWidth={isSelected ? 4 : isHovered ? 3 : 2}
                                        filter={isHovered || isSelected ? 'url(#userGlow)' : undefined}
                                        style={{ transition: 'all 0.3s ease' }}
                                    />

                                    {/* User initials */}
                                    <text
                                        textAnchor="middle"
                                        dy="0.35em"
                                        fill="white"
                                        fontSize="14px"
                                        fontWeight="bold"
                                        style={{ pointerEvents: 'none' }}
                                    >
                                        {getInitials(user.name)}
                                    </text>

                                    {/* Purchase count badge */}
                                    <g transform={`translate(${user.radius - 5}, ${-user.radius + 5})`}>
                                        <circle r="12" fill="#1f2937" stroke="#f59e0b" strokeWidth="2" />
                                        <text textAnchor="middle" dy="0.35em" fill="white" fontSize="9px" fontWeight="bold">
                                            {user.purchase_count}
                                        </text>
                                    </g>
                                </g>
                            );
                        })}
                    </g>

                    {/* Tooltip */}
                    {hoveredNode && !selectedUser && (() => {
                        const user = positionedUsers.find(u => u.id === hoveredNode);
                        if (!user) return null;

                        return (
                            <g transform={`translate(${user.x + user.radius + 15}, ${user.y - 30})`}>
                                <rect width="150" height="60" rx="8" fill="rgba(17, 24, 39, 0.95)" stroke="#f59e0b" strokeWidth="1" />
                                <text x="10" y="18" fill="white" fontSize="12px" fontWeight="600">{user.name}</text>
                                <text x="10" y="35" fill="#9ca3af" fontSize="10px">{user.purchase_count} purchases</text>
                                <text x="10" y="50" fill="#f59e0b" fontSize="9px">Click to see orders →</text>
                            </g>
                        );
                    })()}
                </svg>
            </div>

            {/* Order History Section (shown when user is selected) */}
            {selectedUser && (
                <div style={{
                    background: 'var(--bg-glass)',
                    borderRadius: '12px',
                    border: '2px solid #ec4899',
                    padding: '1.5rem',
                    animation: 'fadeIn 0.3s ease'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>
                            📦 Order History: <span style={{ color: '#ec4899' }}>{selectedUser.name}</span>
                        </h3>
                        <button
                            className="btn btn-secondary"
                            onClick={() => setSelectedUser(null)}
                            style={{ padding: '0.5rem 1rem' }}
                        >
                            ✕ Close
                        </button>
                    </div>

                    {orderData ? (
                        orderData.nodes?.length > 0 ? (
                            <>
                                <p style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.9rem' }}>
                                    {orderData.total_products} products across {orderData.orders?.length || 0} orders.
                                    Each cluster represents products bought together.
                                </p>

                                {/* Order Clusters Graph */}
                                <div style={{
                                    background: 'rgba(0,0,0,0.3)',
                                    borderRadius: '8px',
                                    padding: '1rem',
                                    overflow: 'auto'
                                }}>
                                    <svg width="100%" height={orderHeight} viewBox={`0 0 ${orderWidth} ${orderHeight}`}>
                                        <defs>
                                            <linearGradient id="orderProductGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                                <stop offset="0%" stopColor="#10b981" />
                                                <stop offset="100%" stopColor="#059669" />
                                            </linearGradient>
                                        </defs>

                                        {/* Order labels */}
                                        {orderData.orders?.map((order, idx) => {
                                            const clusterWidth = orderWidth / (orderData.orders.length + 1);
                                            const x = clusterWidth * (idx + 1);
                                            return (
                                                <g key={order.order_id}>
                                                    <text x={x} y="30" textAnchor="middle" fill="#9ca3af" fontSize="12px" fontWeight="600">
                                                        Order #{order.order_number}
                                                    </text>
                                                    <text x={x} y="48" textAnchor="middle" fill="#10b981" fontSize="11px">
                                                        ${order.total.toFixed(2)}
                                                    </text>
                                                    {/* Cluster background */}
                                                    <circle cx={x} cy={orderHeight / 2} r="80" fill="rgba(16, 185, 129, 0.05)" stroke="rgba(16, 185, 129, 0.2)" strokeDasharray="5,5" />
                                                </g>
                                            );
                                        })}

                                        {/* Edges within orders */}
                                        <g className="edges">
                                            {orderData.edges?.map((edge, idx) => {
                                                const source = getOrderNodePosition(edge.source);
                                                const target = getOrderNodePosition(edge.target);
                                                return (
                                                    <line
                                                        key={`order-edge-${idx}`}
                                                        x1={source.x}
                                                        y1={source.y}
                                                        x2={target.x}
                                                        y2={target.y}
                                                        stroke="rgba(16, 185, 129, 0.5)"
                                                        strokeWidth="2"
                                                        strokeLinecap="round"
                                                    />
                                                );
                                            })}
                                        </g>

                                        {/* Product nodes */}
                                        <g className="nodes">
                                            {positionedOrders.map((node) => (
                                                <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
                                                    <circle
                                                        r={node.radius}
                                                        fill="url(#orderProductGradient)"
                                                        stroke="#34d399"
                                                        strokeWidth="2"
                                                    />
                                                    <text
                                                        textAnchor="middle"
                                                        dy="-0.2em"
                                                        fill="white"
                                                        fontSize="9px"
                                                        fontWeight="bold"
                                                        style={{ pointerEvents: 'none' }}
                                                    >
                                                        {getInitials(node.name)}
                                                    </text>
                                                    <text
                                                        textAnchor="middle"
                                                        dy="1em"
                                                        fill="rgba(255,255,255,0.8)"
                                                        fontSize="8px"
                                                        style={{ pointerEvents: 'none' }}
                                                    >
                                                        ${node.price}
                                                    </text>
                                                </g>
                                            ))}
                                        </g>
                                    </svg>
                                </div>

                                {/* Order list */}
                                <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                                    {orderData.orders?.map((order) => (
                                        <div key={order.order_id} style={{
                                            padding: '0.75rem 1rem',
                                            background: 'var(--bg-secondary)',
                                            borderRadius: '8px',
                                            borderLeft: '3px solid #10b981',
                                            fontSize: '0.85rem'
                                        }}>
                                            <strong>Order #{order.order_number}</strong>
                                            <div style={{ color: 'var(--text-muted)' }}>
                                                {order.product_count} items • ${order.total.toFixed(2)}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        ) : (
                            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                                <p>📭 No purchase history for this user yet.</p>
                            </div>
                        )
                    ) : (
                        <div style={{ textAlign: 'center', padding: '2rem' }}>
                            <div className="spinner" style={{ margin: '0 auto' }}></div>
                        </div>
                    )}
                </div>
            )}

            {/* Info box */}
            <div style={{
                marginTop: '1.5rem',
                padding: '1rem',
                background: 'var(--bg-secondary)',
                borderRadius: '8px',
                fontSize: '0.85rem'
            }}>
                <strong>💡 Complete Graph with Jaccard Similarity</strong>
                <p style={{ marginTop: '0.5rem', color: 'var(--text-muted)' }}>
                    This visualization shows <strong>User-User Collaborative Filtering</strong> as a complete graph:
                </p>
                <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
                    <li><strong>Nodes</strong> = Users (size indicates purchase count)</li>
                    <li><strong>Edges</strong> = Jaccard similarity = |A ∩ B| / |A ∪ B| (shared products / total products)</li>
                    <li><strong>Edge color/thickness</strong> = Similarity strength (green = high, gray = low)</li>
                    <li><strong>Click a node</strong> to see their order history as disjoint product clusters</li>
                </ul>
            </div>

            <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `}</style>
        </div>
    );
}

export default UserSimilarityGraph;
