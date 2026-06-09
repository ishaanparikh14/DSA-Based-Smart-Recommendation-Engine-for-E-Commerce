import { useState, useEffect, useRef } from 'react';
import api from '../../api';

/**
 * Heap Visualizer - Binary Tree & Step-by-Step Animation
 */
function HeapVisualizer() {
    const [heap, setHeap] = useState([]);
    const [sorted, setSorted] = useState([]);
    const [message, setMessage] = useState('Click Extract Min to start');
    const [status, setStatus] = useState(null); // 'running', 'success', 'error'
    const [animating, setAnimating] = useState(false);
    const [highlightIndices, setHighlightIndices] = useState([]); // Nodes to highlight (e.g., swapping)
    const [currentStep, setCurrentStep] = useState(null); // 'SWAP', 'POP', 'HEAPIFY'

    // Animation refs
    const intervalRef = useRef(null);
    const speed = 1000; // Animation speed in ms

    // Canvas dimensions
    const width = 1200; // Increased width for better spacing
    const height = 500;

    useEffect(() => {
        return () => stopAnimation();
    }, []);

    const stopAnimation = () => {
        if (intervalRef.current) clearInterval(intervalRef.current);
        setAnimating(false);
        setHighlightIndices([]);
        setCurrentStep(null);
    };

    const handleExtractMin = async () => {
        if (animating) return;

        try {
            setStatus('running');
            setAnimating(true);
            setMessage('🔄 Loading heap data...');
            setHeap([]);
            setSorted([]);

            const res = await api.get('/visualize/heap/extract-min');
            if (!res || !res.data) throw new Error('Invalid response');

            const initialHeap = res.data.initial_structure || [];
            if (initialHeap.length === 0) {
                setMessage('❌ No products available');
                setStatus('error');
                setAnimating(false);
                return;
            }

            // Start Animation Sequence
            setHeap(initialHeap);
            runHeapSortAnimation(initialHeap);

        } catch (err) {
            console.error('Heap error:', err);
            setMessage('⚠️ Failed to load heap');
            setStatus('error');
            setAnimating(false);
        }
    };

    // The main animation runner
    const runHeapSortAnimation = async (initialHeap) => {
        let currentHeap = [...initialHeap];
        let currentSorted = [];

        // Helper to delay steps
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        setMessage(`🔥 Min-Heap Initialized with ${currentHeap.length} items`);
        await delay(1000);

        while (currentHeap.length > 0) {
            // STEP 1: Highlight Root (Min)
            setMessage(`1️⃣ Minimum value found at Root: $${currentHeap[0].score.toFixed(0)}`);
            setHighlightIndices([0]);
            setCurrentStep('MIN_FOUND');
            await delay(speed);

            // STEP 2: Swap Root with Last (if more than 1 item)
            if (currentHeap.length > 1) {
                const lastIdx = currentHeap.length - 1;
                setMessage(`2️⃣ Swap Root ($${currentHeap[0].score.toFixed(0)}) with Last ($${currentHeap[lastIdx].score.toFixed(0)})`);
                setHighlightIndices([0, lastIdx]);
                setCurrentStep('SWAP');
                await delay(speed);

                // Perform Swap in state
                const temp = currentHeap[0];
                currentHeap[0] = currentHeap[lastIdx];
                currentHeap[lastIdx] = temp;
                setHeap([...currentHeap]);
                await delay(speed);
            }

            // STEP 3: Remove Last (which is the min)
            const minItem = currentHeap.pop();
            setMessage(`3️⃣ Extract Min: $${minItem.score.toFixed(0)}`);
            setHeap([...currentHeap]);
            currentSorted.push(minItem);
            setSorted([...currentSorted]);
            setHighlightIndices([]);
            setCurrentStep('POP');
            await delay(speed);

            // STEP 4: Heapify Down (Bubble Down)
            if (currentHeap.length > 0) {
                setMessage('4️⃣ Heapify Down: Restore Min-Heap property');
                setCurrentStep('HEAPIFY');

                let idx = 0;
                while (true) {
                    let left = 2 * idx + 1;
                    let right = 2 * idx + 2;
                    let smallest = idx;

                    // Visualize comparison
                    const indicesToCheck = [idx];
                    if (left < currentHeap.length) indicesToCheck.push(left);
                    if (right < currentHeap.length) indicesToCheck.push(right);
                    setHighlightIndices(indicesToCheck);

                    if (left < currentHeap.length && currentHeap[left].score < currentHeap[smallest].score) {
                        smallest = left;
                    }
                    if (right < currentHeap.length && currentHeap[right].score < currentHeap[smallest].score) {
                        smallest = right;
                    }

                    if (smallest !== idx) {
                        setMessage(`🔻 Swapping down: $${currentHeap[idx].score.toFixed(0)} > $${currentHeap[smallest].score.toFixed(0)}`);
                        await delay(speed * 0.8);

                        // Swap
                        const t = currentHeap[idx];
                        currentHeap[idx] = currentHeap[smallest];
                        currentHeap[smallest] = t;
                        setHeap([...currentHeap]);

                        idx = smallest;
                        await delay(speed * 0.8);
                    } else {
                        break; // Heap property restored
                    }
                }
            }
            setHighlightIndices([]);
        }

        setStatus('success');
        setAnimating(false);
        setMessage('✅ Heap Sort Complete! All items extracted in order.');
    };

    const reset = () => {
        stopAnimation();
        setHeap([]);
        setSorted([]);
        setStatus(null);
        setMessage('Click Extract Min to start');
    };

    // --- Render Helpers ---

    const getTreeCoordinates = (index, total) => {
        const level = Math.floor(Math.log2(index + 1));
        const itemsInLevel = Math.pow(2, level);
        const indexInLevel = index - itemsInLevel + 1;

        // Better distribution for large number of items in last level
        // Use fixed width segments based on max items in the deepest level
        const maxLevel = Math.floor(Math.log2(15)); // Assuming max 15 items
        const maxItems = Math.pow(2, maxLevel);
        const segmentWidth = width / (maxItems + 1);

        // Centre each level
        const levelWidth = width;
        const xOffset = levelWidth / (itemsInLevel + 1);
        const x = xOffset * (indexInLevel + 1);
        const y = 50 + level * 90; // Increased vertical spacing

        return { x, y };
    };

    return (
        <div style={{ padding: '1rem' }}>
            {/* Controls */}
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <button
                    className="btn btn-primary"
                    onClick={handleExtractMin}
                    disabled={animating}
                >
                    {animating ? '⏳ Sorting...' : '🔥 Extract Min (Step-by-Step)'}
                </button>
                {sorted.length > 0 && (
                    <button className="btn btn-secondary" onClick={reset}>
                        🔄 Reset
                    </button>
                )}
            </div>

            {/* Status */}
            <div style={{
                padding: '1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                background: status === 'success' ? 'rgba(16,185,129,0.1)' :
                    status === 'error' ? 'rgba(239,68,68,0.1)' : '#1e293b',
                border: `1px solid ${status === 'success' ? '#10b981' : status === 'error' ? '#ef4444' : '#334155'}`,
                color: status === 'success' ? '#10b981' : status === 'error' ? '#ef4444' : '#e2e8f0',
                fontWeight: 'bold',
                textAlign: 'center',
                minHeight: '60px',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
                {message}
            </div>

            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                {/* Tree Visualization */}
                <div style={{
                    flex: 2,
                    minWidth: '500px',
                    height: '500px',
                    background: '#0f172a',
                    borderRadius: '12px',
                    border: '1px solid #334155',
                    position: 'relative',
                    overflow: 'auto' // Allow scrolling if needed
                }}>
                    <div style={{ minWidth: '1200px', height: '100%' }}> {/* Ensure SVG has enough space */}
                        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
                            {/* Edges */}
                            {heap.map((_, idx) => {
                                if (idx === 0) return null;
                                const parentIdx = Math.floor((idx - 1) / 2);
                                const { x: x1, y: y1 } = getTreeCoordinates(parentIdx, heap.length);
                                const { x: x2, y: y2 } = getTreeCoordinates(idx, heap.length);
                                return (
                                    <line
                                        key={`edge-${idx}`}
                                        x1={x1} y1={y1} x2={x2} y2={y2}
                                        stroke="#334155"
                                        strokeWidth="2"
                                    />
                                );
                            })}

                            {/* Nodes */}
                            {heap.map((node, idx) => {
                                const { x, y } = getTreeCoordinates(idx, heap.length);
                                const isHighlighted = highlightIndices.includes(idx);
                                const isRoot = idx === 0;

                                // Color logic
                                let fill = '#6366f1'; // Default indigo
                                let stroke = '#818cf8';

                                if (isRoot) {
                                    fill = '#ef4444'; // Red for min
                                    stroke = '#f87171';
                                }
                                if (isHighlighted) {
                                    fill = '#f59e0b'; // Amber for active
                                    stroke = '#fbbf24';
                                }

                                return (
                                    <g key={`node-${node.data || idx}`} style={{ transition: 'all 0.5s ease' }}>
                                        <circle
                                            cx={x} cy={y} r="24"
                                            fill={fill}
                                            stroke={stroke}
                                            strokeWidth={isHighlighted ? 4 : 2}
                                        />
                                        <text
                                            x={x} y={y} dy="0.35em"
                                            textAnchor="middle"
                                            fill="white"
                                            fontWeight="bold"
                                            fontSize="12px"
                                        >
                                            ${node.score.toFixed(0)}
                                        </text>

                                        {/* Index label */}
                                        <text
                                            x={x} y={y - 32}
                                            textAnchor="middle"
                                            fill="#64748b"
                                            fontSize="10px"
                                        >
                                            {idx}
                                        </text>
                                    </g>
                                );
                            })}
                        </svg>

                        {heap.length === 0 && !animating && status !== 'error' && (
                            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#64748b' }}>
                                Heap Tree will appear here
                            </div>
                        )}
                    </div>
                </div>

                {/* Sorted List */}
                <div style={{
                    flex: 1,
                    minWidth: '250px',
                    maxHeight: '500px',
                    background: '#1e293b',
                    borderRadius: '12px',
                    border: '1px solid #334155',
                    padding: '1rem',
                    display: 'flex',
                    flexDirection: 'column'
                }}>
                    <h3 style={{ color: '#10b981', marginBottom: '1rem', fontSize: '1.1rem' }}>
                        📊 Sorted (Min First)
                    </h3>
                    <div style={{ overflowY: 'auto', flex: 1, paddingRight: '5px' }}>
                        {sorted.length === 0 && (
                            <p style={{ color: '#64748b', fontSize: '0.9rem', textAlign: 'center', marginTop: '2rem' }}>
                                Extracted items will appear here
                            </p>
                        )}
                        {sorted.map((item, idx) => (
                            <div key={`sorted-${idx}`} style={{
                                padding: '0.5rem',
                                borderBottom: '1px solid #334155',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px',
                                animation: 'fadeIn 0.3s ease-in'
                            }}>
                                <span style={{
                                    background: '#10b981',
                                    color: 'white',
                                    fontSize: '0.8rem',
                                    padding: '2px 6px',
                                    borderRadius: '4px'
                                }}>
                                    #{idx + 1}
                                </span>
                                <span style={{ color: '#e2e8f0', fontSize: '0.9rem', flex: 1 }}>
                                    {item.name || 'Product'}
                                </span>
                                <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>
                                    ${item.score.toFixed(0)}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateX(-10px); }
                    to { opacity: 1; transform: translateX(0); }
                }
            `}</style>
        </div>
    );
}

export default HeapVisualizer;
