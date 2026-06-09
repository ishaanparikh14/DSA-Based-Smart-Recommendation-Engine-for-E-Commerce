import React, { useState, useEffect, useRef } from 'react';
import './ProductSimilarityGraph.css';

const API_BASE_URL = 'http://localhost:5000/api';

const ProductSimilarityGraph = () => {
    const [graphData, setGraphData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);
    const [minSimilarity, setMinSimilarity] = useState(0.15);
    const [maxEdges, setMaxEdges] = useState(5);
    const [categoryFilter, setCategoryFilter] = useState('');
    const [categories, setCategories] = useState([]);
    const [animationStep, setAnimationStep] = useState(0);

    const canvasRef = useRef(null);
    const animationRef = useRef(null);
    const nodesRef = useRef([]);
    const edgesRef = useRef([]);

    // Physics simulation parameters - Adjusted for better spacing
    const physics = {
        centerForce: 0.005,          // Reduced to allow more spread
        repulsionForce: 15000,       // Increased significantly for more spacing
        attractionForce: 0.02,       // Reduced to prevent tight clustering
        damping: 0.85,               // Slightly increased for stability
        maxSpeed: 8,                 // Increased for faster settling
        desiredEdgeLength: 200       // Target distance between connected nodes
    };

    // Fetch categories
    useEffect(() => {
        fetch(`${API_BASE_URL}/categories`)
            .then(res => res.json())
            .then(data => setCategories(data.categories || []))
            .catch(err => console.error('Failed to load categories:', err));
    }, []);

    // Fetch graph data
    useEffect(() => {
        loadGraphData();
    }, [minSimilarity, maxEdges, categoryFilter]);

    const loadGraphData = async () => {
        setLoading(true);
        setError(null);
        setAnimationStep(0);

        try {
            let url = `${API_BASE_URL}/visualize/product-similarity-graph?min_similarity=${minSimilarity}&max_edges=${maxEdges}`;
            if (categoryFilter) {
                url += `&category=${encodeURIComponent(categoryFilter)}`;
            }

            const response = await fetch(url);
            const data = await response.json();

            if (data.nodes && data.nodes.length > 0) {
                // Initialize node positions randomly
                const canvas = canvasRef.current;
                const width = canvas.width;
                const height = canvas.height;
                const centerX = width / 2;
                const centerY = height / 2;

                data.nodes.forEach((node, index) => {
                    const angle = (index / data.nodes.length) * 2 * Math.PI;
                    const radius = Math.min(width, height) * 0.4; // Increased from 0.3 to 0.4
                    // Add some randomness to prevent perfect circle
                    const randomOffset = (Math.random() - 0.5) * 100;
                    node.x = centerX + Math.cos(angle) * radius + randomOffset;
                    node.y = centerY + Math.sin(angle) * radius + randomOffset;
                    node.vx = 0;
                    node.vy = 0;
                    node.radius = 8 + (node.purchaseCount || 0) * 2; // Size based on purchase count
                });

                nodesRef.current = data.nodes;
                edgesRef.current = data.edges;
                setGraphData(data);
            } else {
                setError('No products found with the current filters');
                nodesRef.current = [];
                edgesRef.current = [];
            }

            setLoading(false);
        } catch (err) {
            setError('Failed to load graph data: ' + err.message);
            setLoading(false);
        }
    };

    // Physics simulation
    useEffect(() => {
        if (!graphData || loading) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;

        let frameCount = 0;

        const animate = () => {
            frameCount++;

            // Clear canvas
            ctx.clearRect(0, 0, width, height);

            // Draw background
            ctx.fillStyle = '#0a0e27';
            ctx.fillRect(0, 0, width, height);

            // Apply forces
            const nodes = nodesRef.current;
            const edges = edgesRef.current;

            // Repulsion between nodes
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dx = nodes[j].x - nodes[i].x;
                    const dy = nodes[j].y - nodes[i].y;
                    const distSq = dx * dx + dy * dy;
                    const dist = Math.sqrt(distSq) || 1;

                    // Increased repulsion range for better spacing
                    if (dist < 300) {
                        const force = physics.repulsionForce / (distSq || 1);
                        const fx = (dx / dist) * force;
                        const fy = (dy / dist) * force;

                        nodes[i].vx -= fx;
                        nodes[i].vy -= fy;
                        nodes[j].vx += fx;
                        nodes[j].vy += fy;
                    }
                }
            }

            // Edge attraction
            edges.forEach(edge => {
                const source = nodes.find(n => n.id === edge.source);
                const target = nodes.find(n => n.id === edge.target);

                if (source && target) {
                    const dx = target.x - source.x;
                    const dy = target.y - source.y;
                    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                    // Use desired edge length for more consistent spacing
                    const targetLength = physics.desiredEdgeLength * (1 - edge.weight * 0.3);
                    const force = (dist - targetLength) * physics.attractionForce * edge.weight;

                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;

                    source.vx += fx;
                    source.vy += fy;
                    target.vx -= fx;
                    target.vy -= fy;
                }
            });

            // Center force
            nodes.forEach(node => {
                const dx = centerX - node.x;
                const dy = centerY - node.y;
                node.vx += dx * physics.centerForce;
                node.vy += dy * physics.centerForce;
            });

            // Update positions
            nodes.forEach(node => {
                // Apply damping
                node.vx *= physics.damping;
                node.vy *= physics.damping;

                // Limit speed
                const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
                if (speed > physics.maxSpeed) {
                    node.vx = (node.vx / speed) * physics.maxSpeed;
                    node.vy = (node.vy / speed) * physics.maxSpeed;
                }

                // Update position
                node.x += node.vx;
                node.y += node.vy;

                // Keep within bounds with padding
                const padding = 50;
                node.x = Math.max(padding, Math.min(width - padding, node.x));
                node.y = Math.max(padding, Math.min(height - padding, node.y));
            });

            // Draw edges with animation
            const maxEdgesToShow = Math.min(edges.length, Math.floor(animationStep / 2));
            for (let i = 0; i < maxEdgesToShow; i++) {
                const edge = edges[i];
                const source = nodes.find(n => n.id === edge.source);
                const target = nodes.find(n => n.id === edge.target);

                if (source && target) {
                    // Edge color based on weight
                    const opacity = 0.2 + edge.weight * 0.6;
                    const hue = 200 + edge.weight * 60; // Blue to cyan gradient
                    ctx.strokeStyle = `hsla(${hue}, 70%, 60%, ${opacity})`;
                    ctx.lineWidth = 1 + edge.weight * 3;

                    ctx.beginPath();
                    ctx.moveTo(source.x, source.y);
                    ctx.lineTo(target.x, target.y);
                    ctx.stroke();

                    // Draw edge weight label
                    const midX = (source.x + target.x) / 2;
                    const midY = (source.y + target.y) / 2;
                    ctx.fillStyle = '#ffffff';
                    ctx.font = '10px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText(edge.label, midX, midY);
                }
            }

            // Draw nodes with animation
            const maxNodesToShow = Math.min(nodes.length, Math.floor(animationStep / 3) + 1);
            for (let i = 0; i < maxNodesToShow; i++) {
                const node = nodes[i];
                const isSelected = selectedNode && selectedNode.id === node.id;

                // Glow effect for selected node
                if (isSelected) {
                    ctx.shadowBlur = 20;
                    ctx.shadowColor = '#00ffff';
                }

                // Node circle
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);

                // Color based on category
                const categoryColors = {
                    'Electronics': '#4a90e2',
                    'Fashion': '#e24a90',
                    'Books': '#90e24a',
                    'Home & Kitchen': '#e2904a',
                    'Sports': '#904ae2',
                    'Beauty': '#e2e24a'
                };

                const category = node.category.split('>')[0].trim();
                ctx.fillStyle = categoryColors[category] || '#888888';
                ctx.fill();

                // Border
                ctx.strokeStyle = isSelected ? '#00ffff' : '#ffffff';
                ctx.lineWidth = isSelected ? 3 : 1;
                ctx.stroke();

                ctx.shadowBlur = 0;

                // Node label
                ctx.fillStyle = '#ffffff';
                ctx.font = isSelected ? 'bold 12px Arial' : '11px Arial';
                ctx.textAlign = 'center';
                const labelY = node.y + node.radius + 15;

                // Truncate long names
                const maxLength = 15;
                const label = node.name.length > maxLength
                    ? node.name.substring(0, maxLength) + '...'
                    : node.name;
                ctx.fillText(label, node.x, labelY);

                // Purchase count badge
                if (node.purchaseCount > 0) {
                    ctx.fillStyle = '#ff6b6b';
                    ctx.beginPath();
                    ctx.arc(node.x + node.radius - 3, node.y - node.radius + 3, 8, 0, 2 * Math.PI);
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 10px Arial';
                    ctx.fillText(node.purchaseCount, node.x + node.radius - 3, node.y - node.radius + 7);
                }
            }

            // Update animation step
            if (animationStep < nodes.length * 3 + edges.length * 2) {
                setAnimationStep(prev => prev + 1);
            }

            animationRef.current = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [graphData, loading, selectedNode, animationStep]);

    // Handle canvas click
    const handleCanvasClick = (event) => {
        const canvas = canvasRef.current;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Find clicked node
        const clicked = nodesRef.current.find(node => {
            const dx = x - node.x;
            const dy = y - node.y;
            return Math.sqrt(dx * dx + dy * dy) <= node.radius;
        });

        setSelectedNode(clicked || null);
    };

    return (
        <div className="product-similarity-graph">
            <div className="graph-header">
                <h2>🕸️ Product Similarity Graph</h2>
                <p>Products connected by purchase patterns and similarity scores</p>
            </div>

            <div className="graph-controls">
                <div className="control-group">
                    <label>
                        Minimum Similarity: {minSimilarity.toFixed(2)}
                        <input
                            type="range"
                            min="0.05"
                            max="0.5"
                            step="0.05"
                            value={minSimilarity}
                            onChange={(e) => setMinSimilarity(parseFloat(e.target.value))}
                        />
                    </label>
                </div>

                <div className="control-group">
                    <label>
                        Max Connections: {maxEdges}
                        <input
                            type="range"
                            min="3"
                            max="10"
                            step="1"
                            value={maxEdges}
                            onChange={(e) => setMaxEdges(parseInt(e.target.value))}
                        />
                    </label>
                </div>

                <div className="control-group">
                    <label>
                        Filter by Category:
                        <select
                            value={categoryFilter}
                            onChange={(e) => setCategoryFilter(e.target.value)}
                        >
                            <option value="">All Categories</option>
                            {categories.map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </label>
                </div>

                <button className="reset-btn" onClick={() => setAnimationStep(0)}>
                    🔄 Restart Animation
                </button>
            </div>

            {loading && (
                <div className="loading-state">
                    <div className="spinner"></div>
                    <p>Building similarity graph...</p>
                </div>
            )}

            {error && (
                <div className="error-state">
                    <p>⚠️ {error}</p>
                </div>
            )}

            <div className="graph-container">
                <canvas
                    ref={canvasRef}
                    width={1200}
                    height={700}
                    onClick={handleCanvasClick}
                    className="graph-canvas"
                />

                {selectedNode && (
                    <div className="node-details">
                        <h3>{selectedNode.name}</h3>
                        <p><strong>Category:</strong> {selectedNode.category}</p>
                        <p><strong>Price:</strong> ${selectedNode.price}</p>
                        <p><strong>Purchases:</strong> {selectedNode.purchaseCount || 0}</p>
                        <button onClick={() => setSelectedNode(null)}>Close</button>
                    </div>
                )}

                {graphData && (
                    <div className="graph-stats">
                        <h3>Graph Statistics</h3>
                        <div className="stat-item">
                            <span className="stat-label">Products:</span>
                            <span className="stat-value">{graphData.stats.totalProducts}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Connections:</span>
                            <span className="stat-value">{graphData.stats.totalConnections}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Avg Similarity:</span>
                            <span className="stat-value">{graphData.stats.avgSimilarity.toFixed(3)}</span>
                        </div>
                    </div>
                )}
            </div>

            <div className="graph-legend">
                <h3>Legend</h3>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#4a90e2' }}></span>
                    <span>Electronics</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#e24a90' }}></span>
                    <span>Fashion</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#90e24a' }}></span>
                    <span>Books</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#e2904a' }}></span>
                    <span>Home & Kitchen</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#904ae2' }}></span>
                    <span>Sports</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color" style={{ backgroundColor: '#e2e24a' }}></span>
                    <span>Beauty</span>
                </div>
                <div className="legend-note">
                    <strong>Edge Thickness:</strong> Indicates similarity strength<br />
                    <strong>Node Size:</strong> Based on purchase count<br />
                    <strong>Red Badge:</strong> Number of purchases
                </div>
            </div>
        </div>
    );
};

export default ProductSimilarityGraph;
