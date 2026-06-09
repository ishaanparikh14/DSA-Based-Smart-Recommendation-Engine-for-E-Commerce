import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getStats } from '../api';

function LandingPage({ currentUser }) {
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);

    useEffect(() => {
        getStats()
            .then((response) => {
                setStats(response.data);
            })
            .catch((error) => {
                console.error('Error loading stats:', error);
            });
    }, []);

    return (
        <div className="landing-page">
            {/* Hero Section */}
            <div className="hero-section">
                <h1 className="hero-title">
                    DSA-Driven E-Commerce
                    <br />
                    <span className="gradient-text">Recommendation Engine</span>
                </h1>
                <p className="hero-subtitle">
                    Sophisticated personalized recommendations using ONLY classical Data Structures & Algorithms
                    <br />
                    <strong>NO Machine Learning • 100% Explainable</strong>
                </p>

                <div className="hero-buttons">
                    <button
                        className="btn btn-primary btn-large"
                        onClick={() => navigate('/products')}
                    >
                        Start Shopping
                    </button>
                    <button
                        className="btn btn-secondary btn-large"
                        onClick={() => navigate('/recommendations')}
                    >
                        View Recommendations
                    </button>
                </div>

                {currentUser && (
                    <div className="welcome-message">
                        Welcome back, <strong>{currentUser.name}</strong>! 👋
                    </div>
                )}
            </div>

            {/* Stats Section */}
            {stats && (
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-number">{stats.products}</div>
                        <div className="stat-label">Products</div>
                        <div className="stat-detail">Across {stats.categories} categories</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">8</div>
                        <div className="stat-label">Data Structures</div>
                        <div className="stat-detail">Custom implementations</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">6</div>
                        <div className="stat-label">Pipeline Stages</div>
                        <div className="stat-detail">Category-first algorithm</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">100%</div>
                        <div className="stat-label">Explainable</div>
                        <div className="stat-detail">No black box</div>
                    </div>
                </div>
            )}

            {/* Features Section */}
            <div className="features-section">
                <h2 className="section-title">How It Works</h2>

                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">🔗</div>
                        <h3>Doubly Linked List</h3>
                        <p>Shopping cart with O(1) add/remove operations</p>
                        <div className="feature-tag">Cart Management</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">📚</div>
                        <h3>Stack (LIFO)</h3>
                        <p>Track recently viewed products</p>
                        <div className="feature-tag">View History</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🔄</div>
                        <h3>Queue (FIFO)</h3>
                        <p>Session action tracking</p>
                        <div className="feature-tag">Activity Log</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🌳</div>
                        <h3>Trie (Prefix Tree)</h3>
                        <p>Fast category matching and filtering</p>
                        <div className="feature-tag">Category Filter</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🔍</div>
                        <h3>Binary Search Tree</h3>
                        <p>Price and inventory range queries</p>
                        <div className="feature-tag">Filtering</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">⛰️</div>
                        <h3>Heap</h3>
                        <p>Efficient Top-K recommendation selection</p>
                        <div className="feature-tag">Ranking</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🕸️</div>
                        <h3>Graph</h3>
                        <p>Co-occurrence analysis for "bought together"</p>
                        <div className="feature-tag">Market Basket</div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">⚡</div>
                        <h3>Hash Map</h3>
                        <p>O(1) product catalog lookups</p>
                        <div className="feature-tag">Fast Access</div>
                    </div>
                </div>
            </div>

            {/* Algorithm Section */}
            <div className="algorithm-section">
                <h2 className="section-title">6-Stage Recommendation Pipeline</h2>

                <div className="pipeline-flow">
                    <div className="pipeline-stage">
                        <div className="stage-number">1</div>
                        <div className="stage-content">
                            <h4>Co-Occurrence Graph</h4>
                            <p>Analyze products bought together</p>
                        </div>
                    </div>
                    <div className="pipeline-arrow">→</div>

                    <div className="pipeline-stage">
                        <div className="stage-number">2</div>
                        <div className="stage-content">
                            <h4>Collaborative Filtering</h4>
                            <p>Find similar users (Jaccard)</p>
                        </div>
                    </div>
                    <div className="pipeline-arrow">→</div>

                    <div className="pipeline-stage pipeline-stage-critical">
                        <div className="stage-number">3</div>
                        <div className="stage-content">
                            <h4>Category Filter ⭐</h4>
                            <p>Match user preferences (Trie)</p>
                        </div>
                    </div>
                    <div className="pipeline-arrow">→</div>

                    <div className="pipeline-stage">
                        <div className="stage-number">4</div>
                        <div className="stage-content">
                            <h4>Ranking Engine</h4>
                            <p>Multi-criteria scoring (BST)</p>
                        </div>
                    </div>
                    <div className="pipeline-arrow">→</div>

                    <div className="pipeline-stage">
                        <div className="stage-number">5</div>
                        <div className="stage-content">
                            <h4>Top-K Selection</h4>
                            <p>Heap-based selection</p>
                        </div>
                    </div>
                    <div className="pipeline-arrow">→</div>

                    <div className="pipeline-stage">
                        <div className="stage-number">6</div>
                        <div className="stage-content">
                            <h4>Explainability</h4>
                            <p>Full decision trace</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* CTA Section */}
            <div className="cta-section">
                <h2>Ready to Experience Classical Algorithms?</h2>
                <p>No ML, No AI - Just pure Data Structures & Algorithms</p>
                <button
                    className="btn btn-primary btn-large"
                    onClick={() => navigate('/products')}
                >
                    Start Shopping Now
                </button>
            </div>
        </div>
    );
}

export default LandingPage;
