import { useState, useEffect } from 'react';
import api from '../../api';

/**
 * Trie Visualizer - Rewritten with maximum error handling
 */
function TrieVisualizer() {
    const [prefix, setPrefix] = useState('');
    const [trace, setTrace] = useState([]);
    const [results, setResults] = useState([]);
    const [allCategories, setAllCategories] = useState([]);
    const [message, setMessage] = useState('Enter a prefix to search');
    const [status, setStatus] = useState(null);
    const [animating, setAnimating] = useState(false);
    const [searchedPrefix, setSearchedPrefix] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [intervalRef, setIntervalRef] = useState(null);

    useEffect(() => {
        loadCategories();
        return () => {
            if (intervalRef) clearInterval(intervalRef);
        };
    }, []);

    const loadCategories = async () => {
        try {
            setLoading(true);
            setError(null);
            const res = await api.get('/visualize/trie/search?q=');
            if (res && res.data && res.data.all_categories) {
                setAllCategories(res.data.all_categories);
            }
        } catch (err) {
            console.error('Load categories error:', err);
            // Don't set error - just continue without categories
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!prefix.trim() || animating) return;

        try {
            if (intervalRef) clearInterval(intervalRef);

            setAnimating(true);
            setTrace([]);
            setStatus(null);
            setResults([]);
            setMessage('🔍 Searching...');
            setSearchedPrefix(prefix.toLowerCase().trim());

            const res = await api.get(`/visualize/trie/search?q=${encodeURIComponent(prefix)}`);

            if (!res || !res.data) {
                throw new Error('Invalid response');
            }

            const path = res.data.trace || [];
            const categories = res.data.found_categories || [];
            const respStatus = res.data.status || 'not-found';
            const respMessage = res.data.message || 'Search complete';

            setResults(categories);

            // Animate trace
            if (path.length === 0) {
                setStatus(respStatus);
                setMessage(respMessage);
                setAnimating(false);
                return;
            }

            let i = 0;
            const interval = setInterval(() => {
                if (i >= path.length) {
                    clearInterval(interval);
                    setAnimating(false);
                    setStatus(respStatus);
                    setMessage(respMessage);
                    return;
                }

                const char = path[i];
                if (char !== undefined) {
                    setTrace(prev => [...prev, char]);
                    setMessage(`🔍 Tracing: "${path.slice(0, i + 1).join('')}"`);
                }
                i++;
            }, 350);

            setIntervalRef(interval);
        } catch (err) {
            console.error('Trie search error:', err);
            setMessage('⚠️ Search failed');
            setStatus('error');
            setAnimating(false);
        }
    };

    const resetSearch = () => {
        if (intervalRef) clearInterval(intervalRef);
        setTrace([]);
        setStatus(null);
        setResults([]);
        setMessage('Enter a prefix to search');
        setPrefix('');
        setSearchedPrefix('');
    };

    // LOADING STATE
    if (loading) {
        return (
            <div style={{ padding: '3rem', textAlign: 'center' }}>
                <div className="spinner" style={{ margin: '0 auto 1rem' }}></div>
                <p style={{ color: 'var(--text-muted)' }}>Loading Trie...</p>
            </div>
        );
    }

    const getStatusColor = () => {
        if (status === 'found') return '#10b981';
        if (status === 'not-found' || status === 'error') return '#ef4444';
        if (status === 'partial') return '#f59e0b';
        return '#94a3b8';
    };

    return (
        <div style={{ padding: '1rem' }}>
            {/* Controls */}
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                <input
                    type="text"
                    placeholder="Enter prefix (e.g., el, fa)"
                    value={prefix}
                    onChange={(e) => setPrefix(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    disabled={animating}
                    style={{
                        padding: '0.6rem 1rem',
                        borderRadius: '6px',
                        border: '1px solid #475569',
                        background: '#1e293b',
                        color: 'white',
                        width: '200px'
                    }}
                />
                <button
                    className="btn btn-primary"
                    onClick={handleSearch}
                    disabled={animating || !prefix.trim()}
                >
                    {animating ? '⏳...' : '🔎 Search'}
                </button>
                {(trace.length > 0 || status) && (
                    <button className="btn btn-secondary" onClick={resetSearch}>
                        🔄 Reset
                    </button>
                )}
            </div>

            {/* Categories hint */}
            {allCategories.length > 0 && !status && (
                <div style={{
                    fontSize: '0.8rem',
                    color: '#64748b',
                    marginBottom: '1rem'
                }}>
                    <strong>Try:</strong>{' '}
                    {allCategories.slice(0, 5).map((cat, i) => (
                        <span key={cat}>
                            <button
                                onClick={() => setPrefix(cat.slice(0, 2))}
                                style={{
                                    background: 'none',
                                    border: 'none',
                                    color: '#6366f1',
                                    cursor: 'pointer',
                                    textDecoration: 'underline',
                                    padding: 0
                                }}
                            >
                                {cat}
                            </button>
                            {i < Math.min(allCategories.length, 5) - 1 ? ', ' : ''}
                        </span>
                    ))}
                </div>
            )}

            {/* Status */}
            <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                background: status === 'found' ? 'rgba(16,185,129,0.15)' :
                    status === 'not-found' || status === 'error' ? 'rgba(239,68,68,0.15)' :
                        status === 'partial' ? 'rgba(245,158,11,0.15)' :
                            '#1e293b',
                border: `1px solid ${status ? getStatusColor() : '#334155'}`
            }}>
                <span style={{ fontWeight: status ? '600' : '400', color: getStatusColor() }}>
                    {message}
                </span>
            </div>

            {/* Trie visualization */}
            <div style={{
                background: '#0f172a',
                borderRadius: '8px',
                border: '1px solid #334155',
                padding: '1.5rem',
                minHeight: '100px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
                    {/* Root */}
                    <div style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #6366f1, #4f46e5)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 'bold',
                        fontSize: '0.7rem',
                        color: 'white',
                        border: '2px solid #818cf8',
                        flexShrink: 0
                    }}>
                        ROOT
                    </div>

                    {/* Traced nodes */}
                    {trace.map((char, idx) => {
                        const isLast = idx === trace.length - 1;
                        const nodeColor = status === 'found' && isLast ? '#10b981' :
                            status === 'not-found' && isLast ? '#ef4444' :
                                status === 'partial' && isLast ? '#f59e0b' :
                                    '#10b981';

                        return (
                            <div key={idx} style={{ display: 'flex', alignItems: 'center' }}>
                                <div style={{
                                    width: '30px',
                                    height: '2px',
                                    background: nodeColor
                                }} />
                                <div style={{
                                    width: '45px',
                                    height: '45px',
                                    borderRadius: '50%',
                                    background: nodeColor,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontWeight: 'bold',
                                    fontSize: '1.2rem',
                                    color: 'white',
                                    border: `2px solid ${nodeColor}`,
                                    flexShrink: 0
                                }}>
                                    {String(char).toUpperCase()}
                                </div>
                            </div>
                        );
                    })}

                    {/* Unmatched chars */}
                    {status && searchedPrefix && trace.length < searchedPrefix.length && (
                        searchedPrefix.slice(trace.length).split('').map((char, idx) => (
                            <div key={`unmatched-${idx}`} style={{ display: 'flex', alignItems: 'center' }}>
                                <div style={{ width: '30px', height: '2px', background: '#ef4444', opacity: 0.4 }} />
                                <div style={{
                                    width: '45px',
                                    height: '45px',
                                    borderRadius: '50%',
                                    background: 'transparent',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontWeight: 'bold',
                                    fontSize: '1.2rem',
                                    color: '#ef4444',
                                    border: '2px dashed #ef4444',
                                    opacity: 0.6,
                                    flexShrink: 0
                                }}>
                                    {char.toUpperCase()}
                                </div>
                            </div>
                        ))
                    )}

                    {/* Empty hint */}
                    {trace.length === 0 && !status && (
                        <span style={{ marginLeft: '1rem', color: '#64748b', fontSize: '0.85rem' }}>
                            ← Enter a prefix
                        </span>
                    )}
                </div>
            </div>

            {/* Results */}
            {status === 'found' && results.length > 0 && !animating && (
                <div style={{
                    marginTop: '1rem',
                    padding: '1rem',
                    background: 'rgba(16,185,129,0.1)',
                    borderRadius: '8px',
                    border: '1px solid #10b981'
                }}>
                    <strong style={{ color: '#10b981' }}>
                        ✅ Found {results.length} categories:
                    </strong>
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
                        {results.map((cat, i) => (
                            <span key={i} style={{
                                padding: '0.3rem 0.75rem',
                                background: '#10b981',
                                borderRadius: '15px',
                                color: 'white',
                                fontSize: '0.85rem',
                                fontWeight: '500'
                            }}>
                                {cat}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Legend */}
            <div style={{
                display: 'flex',
                gap: '1.5rem',
                marginTop: '1rem',
                fontSize: '0.8rem',
                color: '#94a3b8',
                flexWrap: 'wrap'
            }}>
                <span style={{ color: '#6366f1' }}>🟣 Root</span>
                <span style={{ color: '#10b981' }}>🟢 Matched</span>
                <span style={{ color: '#f59e0b' }}>🟠 Partial</span>
                <span style={{ color: '#ef4444' }}>🔴 Not Found</span>
            </div>
        </div>
    );
}

export default TrieVisualizer;
