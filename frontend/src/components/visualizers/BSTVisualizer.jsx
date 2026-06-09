import { useState, useEffect } from 'react';
import api from '../../api';

/**
 * BST Visualizer (Rebuild)
 * Optimized for displaying a smaller, readable tree (~25 nodes).
 */
const BSTVisualizer = () => {
    // State
    const [tree, setTree] = useState(null);
    const [searchVal, setSearchVal] = useState('');
    const [status, setStatus] = useState('IDLE'); // IDLE, SEARCHING, FOUND, NOT_FOUND
    const [tracePath, setTracePath] = useState([]);
    const [currentStep, setCurrentStep] = useState(-1);
    const [message, setMessage] = useState('Enter a price to search');

    // Canvas config
    const nodeRadius = 24;
    const verticalSpacing = 70;
    const canvasWidth = 1000;
    const canvasHeight = 600;

    useEffect(() => {
        fetchTreeStructure();
    }, []);

    const fetchTreeStructure = async () => {
        try {
            const res = await api.get('/visualize/bst/structure');
            if (res.data) {
                setTree(res.data);
            }
        } catch (err) {
            console.error(err);
            setMessage('Error loading tree structure');
        }
    };

    const handleSearch = async () => {
        if (!searchVal) return;

        try {
            setStatus('SEARCHING');
            setTracePath([]);
            setCurrentStep(-1);
            setMessage(`Searching for $${searchVal}...`);

            const res = await api.get(`/visualize/bst/search?price=${searchVal}`);
            const { trace, found } = res.data;

            if (trace && trace.length > 0) {
                animateSearch(trace, found);
            } else {
                setMessage('Empty tree or no trace data');
                setStatus('IDLE');
            }
        } catch (err) {
            console.error('Search error:', err);
            setMessage('⚠️ Search failed - please try again');
            setStatus('IDLE');
        }
    };

    const animateSearch = (trace, found) => {
        let step = 0;
        const interval = setInterval(() => {
            if (step >= trace.length) {
                clearInterval(interval);
                setStatus(found ? 'FOUND' : 'NOT_FOUND');
                setMessage(found
                    ? `✅ SUCCESS! Found product with price $${searchVal}`
                    : `❌ NOT FOUND! Price $${searchVal} does not exist in the tree`);
                return;
            }

            const node = trace[step];
            if (!node || typeof node.id === 'undefined') {
                console.error('Invalid node in trace:', node);
                step++;
                return;
            }

            setTracePath(prev => [...prev, node.id]);
            setCurrentStep(step);

            // Helpful message for the step
            const target = parseFloat(searchVal);
            if (node.price === target) {
                setMessage(`🎯 Match found! $${node.price} === $${target}`);
            } else if (target < node.price) {
                setMessage(`👇 $${target} < $${node.price}, searching LEFT subtree...`);
            } else {
                setMessage(`👉 $${target} > $${node.price}, searching RIGHT subtree...`);
            }

            step++;
        }, 800);
    };

    const reset = () => {
        setStatus('IDLE');
        setTracePath([]);
        setCurrentStep(-1);
        setMessage('Enter a price to search');
        setSearchVal('');
    };

    // --- Rendering Logic ---

    // Recursive helper to render tree
    // We pass x, y, and the available width "slice" available to this node's subtree
    const renderTree = (node, x, y, availableWidth) => {
        if (!node) return null;

        // Calculate child positions
        // The child offset should be half of the available width for its side
        // But we clamp it to not be too wide or too narrow
        const childOffset = Math.max(availableWidth / 2.2, 30);

        const leftX = x - childOffset;
        const rightX = x + childOffset;
        const nextY = y + verticalSpacing;

        // Determine node style based on state
        // SAFEGUARD: Ensure node and node.id exist
        const nodeId = node.id;
        const isVisited = tracePath.includes(nodeId);
        const isLastVisited = tracePath.length > 0 && tracePath[tracePath.length - 1] === nodeId;

        let fillColor = '#1e293b'; // Default dark slate
        let strokeColor = '#475569'; // Default border
        let textColor = '#e2e8f0';

        if (isVisited) {
            fillColor = '#3b82f6'; // Blue visited
            strokeColor = '#60a5fa';
        }

        if (isLastVisited) {
            if (status === 'FOUND') {
                fillColor = '#10b981'; // Green Success
                strokeColor = '#34d399';
            } else if (status === 'NOT_FOUND') {
                fillColor = '#ef4444'; // Red Fail represents "stopped here"
                strokeColor = '#f87171';
            } else {
                fillColor = '#eab308'; // Yellow/Orange currently processing
                strokeColor = '#fde047';
                textColor = '#000';
            }
        }

        return (
            <g key={node.id}>
                {/* Edges to children */}
                {node.left && (
                    <line
                        x1={x} y1={y}
                        x2={leftX} y2={nextY}
                        stroke="#334155"
                        strokeWidth="2"
                    />
                )}
                {node.right && (
                    <line
                        x1={x} y1={y}
                        x2={rightX} y2={nextY}
                        stroke="#334155"
                        strokeWidth="2"
                    />
                )}

                {/* Recursively render children first (so lines are behind nodes) */}
                {renderTree(node.left, leftX, nextY, availableWidth * 0.55)}
                {renderTree(node.right, rightX, nextY, availableWidth * 0.55)}

                {/* The Node Itself */}
                <circle
                    cx={x} cy={y} r={nodeRadius}
                    fill={fillColor}
                    stroke={strokeColor}
                    strokeWidth="3"
                    className="transition-colors duration-300"
                />
                <text
                    x={x} y={y}
                    dy="0.35em"
                    textAnchor="middle"
                    fill={textColor}
                    fontSize="12px"
                    fontWeight="bold"
                    style={{ pointerEvents: 'none' }}
                >
                    ${node.value}
                </text>
            </g>
        );
    };

    return (
        <div style={{ padding: '1.5rem', fontFamily: 'Inter, sans-serif' }}>
            {/* Header / Controls */}
            <div style={{
                display: 'flex',
                gap: '1rem',
                alignItems: 'center',
                marginBottom: '1rem',
                background: '#0f172a',
                padding: '1rem',
                borderRadius: '12px',
                border: '1px solid #1e293b'
            }}>
                <div style={{ flex: 1 }}>
                    <h3 style={{ margin: 0, color: '#f8fafc' }}>Top Product Prices BST</h3>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#94a3b8' }}>
                        Visualizing binary search on a subset of products.
                    </p>
                </div>

                {/* Search Box */}
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <input
                        type="number"
                        placeholder="Price..."
                        value={searchVal}
                        onChange={e => setSearchVal(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && handleSearch()}
                        disabled={status === 'SEARCHING'}
                        style={{
                            background: '#1e293b', border: '1px solid #334155',
                            color: '#fff', padding: '0.5rem 1rem', borderRadius: '6px',
                            width: '120px'
                        }}
                    />
                    <button
                        onClick={handleSearch}
                        disabled={status === 'SEARCHING' || !searchVal}
                        className="btn btn-primary"
                    >
                        {status === 'SEARCHING' ? 'Running...' : 'Search'}
                    </button>
                    {status !== 'IDLE' && status !== 'SEARCHING' && (
                        <button onClick={reset} className="btn btn-secondary">
                            Reset
                        </button>
                    )}
                </div>
            </div>

            {/* Message Bar - Large and Prominent */}
            <div style={{
                textAlign: 'center',
                padding: status === 'FOUND' || status === 'NOT_FOUND' ? '1.5rem' : '1rem',
                background: status === 'FOUND' ? 'linear-gradient(135deg, rgba(16,185,129, 0.2), rgba(5,150,105, 0.3))' :
                    status === 'NOT_FOUND' ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.3))' : '#1e293b',
                border: `${status === 'FOUND' || status === 'NOT_FOUND' ? '3px' : '1px'} solid ${status === 'FOUND' ? '#10b981' :
                    status === 'NOT_FOUND' ? '#ef4444' : '#334155'
                    }`,
                borderRadius: '12px',
                color: status === 'FOUND' ? '#10b981' :
                    status === 'NOT_FOUND' ? '#ef4444' : '#e2e8f0',
                fontWeight: '700',
                fontSize: status === 'FOUND' || status === 'NOT_FOUND' ? '1.4rem' : '1.1rem',
                marginBottom: '1.5rem',
                boxShadow: status === 'FOUND' ? '0 0 30px rgba(16,185,129, 0.4)' :
                    status === 'NOT_FOUND' ? '0 0 30px rgba(239, 68, 68, 0.4)' : 'none',
                transition: 'all 0.3s ease',
                letterSpacing: status === 'FOUND' || status === 'NOT_FOUND' ? '0.5px' : 'normal'
            }}>
                {message}
            </div>

            {/* Visualization Area */}
            <div style={{
                background: '#020617',
                borderRadius: '12px',
                border: '1px solid #1e293b',
                overflow: 'auto', // Scroll if needed
                display: 'flex',
                justifyContent: 'center'
            }}>
                {tree ? (
                    <div style={{ minWidth: canvasWidth, padding: '2rem 0' }}>
                        <svg width={canvasWidth} height={canvasHeight} viewBox={`0 0 ${canvasWidth} ${canvasHeight}`}>
                            {renderTree(tree, canvasWidth / 2, 40, canvasWidth / 3)}
                        </svg>
                    </div>
                ) : (
                    <div style={{ padding: '3rem', color: '#64748b' }}>
                        Loading Tree Data...
                    </div>
                )}
            </div>

            {/* Legend */}
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', justifyContent: 'center', fontSize: '0.85rem', color: '#64748b' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#1e293b', border: '1px solid #475569' }}></span> Node
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3b82f6' }}></span> Visited
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#eab308' }}></span> Current
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981' }}></span> Found
                </span>
            </div>
        </div>
    );
};

export default BSTVisualizer;
