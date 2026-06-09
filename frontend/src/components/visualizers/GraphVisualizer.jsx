import { useState, useEffect, useRef, useCallback } from 'react';
import { getRecommendationGraph, getUserProductGraph } from '../../api';

/**
 * GraphVisualizer - Animated recommendation graph visualization
 * Two views:
 * 1. Product Recommendation Graph: Cart items → Recommended products
 * 2. User-Product Graph: All users ↔ Products (shows purchase patterns)
 */
function GraphVisualizer({ userId, cartItems = [], onRefresh }) {
    const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
    const [loading, setLoading] = useState(true);
    const [hoveredNode, setHoveredNode] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);
    const [viewMode, setViewMode] = useState('recommendation'); // 'recommendation' or 'user-product'
    const svgRef = useRef(null);
    const [dimensions, setDimensions] = useState({ width: 900, height: 500 });

    // Fetch graph data based on view mode
    const fetchGraphData = useCallback(async () => {
        if (!userId) return;

        try {
            setLoading(true);
            let response;
            if (viewMode === 'recommendation') {
                response = await getRecommendationGraph(userId);
            } else {
                response = await getUserProductGraph(userId);
            }
            setGraphData(response.data);
        } catch (error) {
            console.error('Error fetching graph:', error);
        } finally {
            setLoading(false);
        }
    }, [userId, viewMode]);

    useEffect(() => {
        fetchGraphData();
    }, [fetchGraphData, cartItems.length]);

    // Calculate node positions for RECOMMENDATION view
    const calculateRecommendationLayout = useCallback(() => {
        const { nodes, edges } = graphData;
        if (nodes.length === 0) return [];

        const width = dimensions.width;
        const height = dimensions.height;
        const centerX = width * 0.2;
        const centerY = height / 2;

        const cartNodes = nodes.filter(n => n.type === 'cart');
        const recNodes = nodes.filter(n => n.type !== 'cart');

        const cartSpacing = Math.min(100, (height - 100) / Math.max(cartNodes.length, 1));
        const cartStartY = centerY - (cartNodes.length - 1) * cartSpacing / 2;

        const positionedNodes = [];

        cartNodes.forEach((node, i) => {
            positionedNodes.push({
                ...node,
                x: centerX,
                y: cartStartY + i * cartSpacing,
                radius: 45,
            });
        });

        const categories = [...new Set(recNodes.map(n => n.category))];
        const categoryGroups = {};

        recNodes.forEach(node => {
            if (!categoryGroups[node.category]) {
                categoryGroups[node.category] = [];
            }
            categoryGroups[node.category].push(node);
        });

        const rightX = width * 0.7;
        const catSpacing = height / (categories.length + 1);

        categories.forEach((cat, catIndex) => {
            const catY = catSpacing * (catIndex + 1);
            const nodesInCat = categoryGroups[cat];
            const nodeSpacing = Math.min(80, 200 / Math.max(nodesInCat.length, 1));
            const startX = rightX - (nodesInCat.length - 1) * nodeSpacing / 2;

            nodesInCat.forEach((node, nodeIndex) => {
                const jitterX = (Math.random() - 0.5) * 20;
                const jitterY = (Math.random() - 0.5) * 20;

                positionedNodes.push({
                    ...node,
                    x: startX + nodeIndex * nodeSpacing + jitterX,
                    y: catY + jitterY,
                    radius: node.type === 'recommendation' ? 35 : 30,
                });
            });
        });

        return positionedNodes;
    }, [graphData, dimensions]);

    // Calculate node positions for USER-PRODUCT view
    const calculateUserProductLayout = useCallback(() => {
        const { nodes, edges } = graphData;
        if (nodes.length === 0) return [];

        const width = dimensions.width;
        const height = dimensions.height;

        const userNodes = nodes.filter(n => n.type === 'user' || n.type === 'current_user');
        const productNodes = nodes.filter(n => n.type === 'product' || n.type === 'cart_product');

        const positionedNodes = [];

        // Position users on the left
        const userSpacing = (height - 80) / Math.max(userNodes.length, 1);
        const userX = width * 0.15;

        userNodes.forEach((node, i) => {
            positionedNodes.push({
                ...node,
                x: userX,
                y: 40 + i * userSpacing + userSpacing / 2,
                radius: node.type === 'current_user' ? 40 : 30,
            });
        });

        // Position products on the right, grouped by category
        const categories = [...new Set(productNodes.map(n => n.category))];
        const categoryGroups = {};

        productNodes.forEach(node => {
            if (!categoryGroups[node.category]) {
                categoryGroups[node.category] = [];
            }
            categoryGroups[node.category].push(node);
        });

        const productX = width * 0.75;
        let currentY = 40;

        categories.forEach((cat) => {
            const nodesInCat = categoryGroups[cat];
            const spacing = 50;

            nodesInCat.forEach((node, idx) => {
                const xOffset = (idx % 2) * 60 - 30; // Stagger horizontally
                positionedNodes.push({
                    ...node,
                    x: productX + xOffset,
                    y: currentY,
                    radius: node.type === 'cart_product' ? 35 : 28,
                });
                currentY += spacing;
            });
        });

        return positionedNodes;
    }, [graphData, dimensions]);

    const positionedNodes = viewMode === 'recommendation'
        ? calculateRecommendationLayout()
        : calculateUserProductLayout();

    // Get node position by ID
    const getNodePosition = (nodeId) => {
        const node = positionedNodes.find(n => n.id === nodeId);
        return node ? { x: node.x, y: node.y } : { x: 0, y: 0 };
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

    // Get node color based on type
    const getNodeColor = (node) => {
        if (node.type === 'cart' || node.type === 'cart_product') {
            return { fill: 'url(#cartGradient)', stroke: '#a855f7' };
        }
        if (node.type === 'current_user') {
            return { fill: 'url(#currentUserGradient)', stroke: '#ec4899' };
        }
        if (node.type === 'user') {
            return { fill: 'url(#userGradient)', stroke: '#f59e0b' };
        }
        if (node.type === 'recommendation') {
            return { fill: 'url(#recGradient)', stroke: '#3b82f6' };
        }
        if (node.type === 'product') {
            return { fill: 'url(#productGradient)', stroke: '#10b981' };
        }
        return { fill: 'url(#catGradient)', stroke: '#10b981' };
    };

    // Get edge color
    const getEdgeColor = (edge, isHighlighted) => {
        if (edge.type === 'cart') {
            return 'rgba(168, 85, 247, 0.8)';
        }
        if (edge.type === 'purchase' && edge.is_current_user) {
            return 'rgba(236, 72, 153, 0.7)';
        }
        if (edge.type === 'co_occurrence') {
            return `rgba(99, 102, 241, ${isHighlighted ? 0.9 : 0.5})`;
        }
        return 'rgba(148, 163, 184, 0.3)';
    };

    // Get edge width
    const getEdgeWidth = (edge) => {
        if (edge.type === 'cart') return 4;
        if (edge.is_current_user) return 3;
        return Math.max(1, Math.min(edge.weight * 1.5, 4));
    };

    if (loading) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <div className="spinner" style={{ margin: '0 auto' }}></div>
                <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>
                    Loading {viewMode === 'recommendation' ? 'recommendation' : 'user-product'} graph...
                </p>
            </div>
        );
    }

    if (graphData.nodes.length === 0) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛒</div>
                <h3>Add items to cart to see the graph</h3>
                <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                    The graph shows how products are connected
                </p>
            </div>
        );
    }

    return (
        <div>
            {/* View Mode Toggle */}
            <div style={{
                display: 'flex',
                gap: '0.5rem',
                marginBottom: '1rem',
                background: 'var(--bg-secondary)',
                padding: '0.5rem',
                borderRadius: '8px',
                width: 'fit-content'
            }}>
                <button
                    className={`btn ${viewMode === 'recommendation' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setViewMode('recommendation')}
                    style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                >
                    📊 Product Recommendations
                </button>
                <button
                    className={`btn ${viewMode === 'user-product' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setViewMode('user-product')}
                    style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                >
                    👥 User-Product Graph
                </button>
            </div>

            {/* Stats */}
            <div style={{
                display: 'flex',
                gap: '1.5rem',
                marginBottom: '1rem',
                fontSize: '0.85rem',
                color: 'var(--text-secondary)'
            }}>
                {viewMode === 'recommendation' ? (
                    <>
                        <span>🛒 {graphData.cart_count} cart items</span>
                        <span>→</span>
                        <span>✨ {graphData.recommendation_count} recommendations</span>
                    </>
                ) : (
                    <>
                        <span>👥 {graphData.user_count} users</span>
                        <span>↔</span>
                        <span>📦 {graphData.product_count} products</span>
                        {graphData.cart_items?.length > 0 && (
                            <span style={{ color: '#a855f7' }}>🛒 {graphData.cart_items.length} in cart</span>
                        )}
                    </>
                )}
                <button
                    onClick={fetchGraphData}
                    style={{
                        marginLeft: 'auto',
                        background: 'none',
                        border: 'none',
                        color: 'var(--primary)',
                        cursor: 'pointer',
                        fontSize: '0.85rem'
                    }}
                >
                    🔄 Refresh
                </button>
            </div>

            {/* Legend */}
            <div style={{
                display: 'flex',
                gap: '1.5rem',
                marginBottom: '1rem',
                fontSize: '0.8rem',
                color: 'var(--text-secondary)',
                flexWrap: 'wrap'
            }}>
                {viewMode === 'recommendation' ? (
                    <>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #a855f7, #7c3aed)',
                            }}></div>
                            <span>Cart Items</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                            }}></div>
                            <span>Co-occurrence</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #10b981, #059669)',
                            }}></div>
                            <span>Category Match</span>
                        </div>
                    </>
                ) : (
                    <>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #ec4899, #be185d)',
                            }}></div>
                            <span>Current User</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                            }}></div>
                            <span>Other Users</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #a855f7, #7c3aed)',
                            }}></div>
                            <span>Cart Products</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{
                                width: '14px', height: '14px', borderRadius: '50%',
                                background: 'linear-gradient(135deg, #10b981, #059669)',
                            }}></div>
                            <span>Products</span>
                        </div>
                    </>
                )}
            </div>

            {/* SVG Graph */}
            <svg
                ref={svgRef}
                width="100%"
                height={dimensions.height}
                viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
                style={{
                    background: 'rgba(0, 0, 0, 0.2)',
                    borderRadius: '12px',
                    overflow: 'visible'
                }}
            >
                {/* Gradient Definitions */}
                <defs>
                    <linearGradient id="cartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#a855f7" />
                        <stop offset="100%" stopColor="#7c3aed" />
                    </linearGradient>

                    <linearGradient id="recGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="100%" stopColor="#1d4ed8" />
                    </linearGradient>

                    <linearGradient id="catGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" />
                        <stop offset="100%" stopColor="#059669" />
                    </linearGradient>

                    <linearGradient id="currentUserGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ec4899" />
                        <stop offset="100%" stopColor="#be185d" />
                    </linearGradient>

                    <linearGradient id="userGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#f59e0b" />
                        <stop offset="100%" stopColor="#d97706" />
                    </linearGradient>

                    <linearGradient id="productGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" />
                        <stop offset="100%" stopColor="#059669" />
                    </linearGradient>

                    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {/* Column Labels for User-Product View */}
                {viewMode === 'user-product' && (
                    <>
                        <text x={dimensions.width * 0.15} y="25" textAnchor="middle" fill="#9ca3af" fontSize="14" fontWeight="600">
                            👥 USERS
                        </text>
                        <text x={dimensions.width * 0.75} y="25" textAnchor="middle" fill="#9ca3af" fontSize="14" fontWeight="600">
                            📦 PRODUCTS
                        </text>
                    </>
                )}

                {/* Edges */}
                <g className="edges">
                    {graphData.edges.map((edge, index) => {
                        const source = getNodePosition(edge.source);
                        const target = getNodePosition(edge.target);
                        const isHighlighted = hoveredNode &&
                            (edge.source === hoveredNode || edge.target === hoveredNode);

                        // Calculate curve for edge
                        const midX = (source.x + target.x) / 2;
                        const midY = (source.y + target.y) / 2;

                        return (
                            <g key={`edge-${index}`}>
                                <line
                                    x1={source.x}
                                    y1={source.y}
                                    x2={target.x}
                                    y2={target.y}
                                    stroke={getEdgeColor(edge, isHighlighted)}
                                    strokeWidth={isHighlighted ? getEdgeWidth(edge) + 2 : getEdgeWidth(edge)}
                                    strokeLinecap="round"
                                    opacity={isHighlighted ? 1 : (edge.is_current_user ? 0.8 : 0.4)}
                                    strokeDasharray={edge.type === 'cart' ? '5 3' : 'none'}
                                    style={{
                                        transition: 'all 0.3s ease',
                                        animation: edge.type === 'cart' || edge.is_current_user
                                            ? 'flowAnimation 1s linear infinite'
                                            : 'none',
                                    }}
                                />
                            </g>
                        );
                    })}
                </g>

                {/* Nodes */}
                <g className="nodes">
                    {positionedNodes.map((node, index) => {
                        const colors = getNodeColor(node);
                        const isHovered = hoveredNode === node.id;
                        const isSpecial = node.type === 'cart' || node.type === 'current_user' || node.type === 'cart_product';

                        return (
                            <g
                                key={node.id}
                                transform={`translate(${node.x}, ${node.y})`}
                                onMouseEnter={() => setHoveredNode(node.id)}
                                onMouseLeave={() => setHoveredNode(null)}
                                style={{ cursor: 'pointer' }}
                            >
                                {/* Node circle */}
                                <circle
                                    r={isHovered ? node.radius * 1.1 : node.radius}
                                    fill={colors.fill}
                                    stroke={colors.stroke}
                                    strokeWidth={isHovered ? 4 : 2}
                                    filter={isHovered ? "url(#glow)" : undefined}
                                    style={{
                                        transition: 'all 0.3s ease',
                                        animation: isSpecial ? 'pulse 2s ease-in-out infinite' : undefined,
                                    }}
                                >
                                    <animate
                                        attributeName="r"
                                        from="0"
                                        to={node.radius}
                                        dur="0.4s"
                                        begin={`${index * 0.03}s`}
                                        fill="freeze"
                                        calcMode="spline"
                                        keySplines="0.34 1.56 0.64 1"
                                    />
                                </circle>

                                {/* Node label */}
                                <text
                                    textAnchor="middle"
                                    dy="0.35em"
                                    fill="white"
                                    fontSize={node.radius > 35 ? "14px" : "11px"}
                                    fontWeight="600"
                                    style={{ pointerEvents: 'none' }}
                                >
                                    {getInitials(node.name)}
                                </text>

                                {/* Badge for special nodes */}
                                {node.type === 'cart' && (
                                    <g transform={`translate(${node.radius - 8}, ${-node.radius + 8})`}>
                                        <circle r="10" fill="#ec4899" stroke="white" strokeWidth="2" />
                                        <text textAnchor="middle" dy="0.35em" fill="white" fontSize="8px">🛒</text>
                                    </g>
                                )}
                                {node.type === 'current_user' && (
                                    <g transform={`translate(${node.radius - 8}, ${-node.radius + 8})`}>
                                        <circle r="10" fill="#10b981" stroke="white" strokeWidth="2" />
                                        <text textAnchor="middle" dy="0.35em" fill="white" fontSize="8px">★</text>
                                    </g>
                                )}
                                {node.type === 'cart_product' && (
                                    <g transform={`translate(${node.radius - 8}, ${-node.radius + 8})`}>
                                        <circle r="10" fill="#ec4899" stroke="white" strokeWidth="2" />
                                        <text textAnchor="middle" dy="0.35em" fill="white" fontSize="8px">🛒</text>
                                    </g>
                                )}

                                {/* Score badge */}
                                {node.total_score && (
                                    <g transform={`translate(${node.radius - 6}, ${node.radius - 6})`}>
                                        <circle r="9" fill="#1f2937" stroke={colors.stroke} strokeWidth="1" />
                                        <text textAnchor="middle" dy="0.35em" fill="white" fontSize="7px" fontWeight="bold">
                                            {node.total_score.toFixed(1)}
                                        </text>
                                    </g>
                                )}
                            </g>
                        );
                    })}
                </g>

                {/* Tooltip */}
                {hoveredNode && (() => {
                    const node = positionedNodes.find(n => n.id === hoveredNode);
                    if (!node) return null;

                    const tooltipWidth = 180;
                    const tooltipHeight = 75;
                    let tooltipX = node.x + node.radius + 10;
                    let tooltipY = node.y - tooltipHeight / 2;

                    if (tooltipX + tooltipWidth > dimensions.width) {
                        tooltipX = node.x - node.radius - tooltipWidth - 10;
                    }
                    if (tooltipY < 10) tooltipY = 10;
                    if (tooltipY + tooltipHeight > dimensions.height - 10) {
                        tooltipY = dimensions.height - tooltipHeight - 10;
                    }

                    return (
                        <g transform={`translate(${tooltipX}, ${tooltipY})`}>
                            <rect
                                width={tooltipWidth}
                                height={tooltipHeight}
                                rx="8"
                                fill="rgba(17, 24, 39, 0.95)"
                                stroke="rgba(99, 102, 241, 0.5)"
                                strokeWidth="1"
                            />
                            <text x="10" y="18" fill="white" fontSize="11px" fontWeight="600">
                                {node.name?.length > 22 ? node.name.substring(0, 22) + '...' : node.name}
                            </text>
                            <text x="10" y="35" fill="#9ca3af" fontSize="10px">
                                {node.category || (node.type.includes('user') ? `${node.purchase_count || 0} purchases` : '')}
                            </text>
                            {node.price && (
                                <text x="10" y="52" fill="#10b981" fontSize="11px" fontWeight="600">
                                    ${node.price?.toFixed(2)}
                                </text>
                            )}
                            <text x={node.price ? 80 : 10} y="52" fill="#6366f1" fontSize="9px">
                                {node.type === 'cart' ? '🛒 In Cart' :
                                    node.type === 'current_user' ? '⭐ You' :
                                        node.type === 'user' ? '👤 User' :
                                            node.type === 'cart_product' ? '🛒 In Cart' :
                                                node.type === 'recommendation' ? '✨ Recommended' : '📦 Product'}
                            </text>
                        </g>
                    );
                })()}
            </svg>

            {/* Info box */}
            <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: 'var(--bg-secondary)',
                borderRadius: '8px',
                fontSize: '0.85rem'
            }}>
                {viewMode === 'recommendation' ? (
                    <>
                        <strong>💡 Product Recommendation Graph</strong>
                        <p style={{ marginTop: '0.5rem', color: 'var(--text-muted)' }}>
                            Shows <strong>Co-Occurrence Graph</strong>: Products in your cart (left) connected to
                            recommended products (right) based on <em>market basket analysis</em>.
                        </p>
                    </>
                ) : (
                    <>
                        <strong>💡 User-Product Graph (Collaborative Filtering)</strong>
                        <p style={{ marginTop: '0.5rem', color: 'var(--text-muted)' }}>
                            Shows all users (left) connected to products (right) by purchase history.
                            Your edges are <span style={{ color: '#ec4899' }}>highlighted pink</span>.
                            Add items to cart to see the graph update live!
                        </p>
                        {graphData.similar_users?.length > 0 && (
                            <p style={{ marginTop: '0.5rem', color: 'var(--text-secondary)' }}>
                                <strong>Similar users:</strong> {graphData.similar_users.map(u => u.user_id).join(', ')}
                            </p>
                        )}
                    </>
                )}
            </div>

            {/* CSS for animations */}
            <style>{`
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.03); }
                }
                
                @keyframes flowAnimation {
                    from { stroke-dashoffset: 0; }
                    to { stroke-dashoffset: -16; }
                }
            `}</style>
        </div>
    );
}

export default GraphVisualizer;
