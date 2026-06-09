import { useState } from 'react';
import ErrorBoundary from './ErrorBoundary';
import BSTVisualizer from './visualizers/BSTVisualizer';
import HeapVisualizer from './visualizers/HeapVisualizer';
import TrieVisualizer from './visualizers/TrieVisualizer';
import UserSimilarityGraph from './visualizers/UserSimilarityGraph';

function Animations({ currentUser }) {
    const [activeTab, setActiveTab] = useState('bst');

    const renderVisualizer = () => {
        switch (activeTab) {
            case 'bst':
                return (
                    <ErrorBoundary key="bst">
                        <BSTVisualizer />
                    </ErrorBoundary>
                );
            case 'heap':
                return (
                    <ErrorBoundary key="heap">
                        <HeapVisualizer />
                    </ErrorBoundary>
                );
            case 'trie':
                return (
                    <ErrorBoundary key="trie">
                        <TrieVisualizer />
                    </ErrorBoundary>
                );
            case 'similarity':
                return (
                    <ErrorBoundary key="similarity">
                        <UserSimilarityGraph />
                    </ErrorBoundary>
                );
            default:
                return (
                    <ErrorBoundary key="default">
                        <BSTVisualizer />
                    </ErrorBoundary>
                );
        }
    };

    return (
        <div className="animations-page container">
            <h1 style={{ textAlign: 'center', margin: '2rem 0' }}>✨ DSA Animations</h1>
            <p style={{ textAlign: 'center', color: '#888', marginBottom: '2rem' }}>
                Interactive visualizations of DSA concepts
            </p>

            {/* Tabs */}
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                gap: '8px',
                marginBottom: '1.5rem',
                flexWrap: 'wrap'
            }}>
                <button
                    className={`btn ${activeTab === 'bst' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('bst')}
                >
                    🌳 BST
                </button>
                <button
                    className={`btn ${activeTab === 'heap' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('heap')}
                >
                    🔥 Heap
                </button>
                <button
                    className={`btn ${activeTab === 'trie' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('trie')}
                >
                    🔎 Trie
                </button>
                <button
                    className={`btn ${activeTab === 'similarity' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('similarity')}
                    style={{
                        background: activeTab === 'similarity' ? 'linear-gradient(135deg, #f59e0b, #d97706)' : undefined,
                        border: activeTab !== 'similarity' ? '1px solid #f59e0b' : undefined
                    }}
                >
                    👥 Users
                </button>
            </div>

            {/* Visualizer Container */}
            <div className="glass-card" style={{ minHeight: '450px', padding: '1rem' }}>
                {renderVisualizer()}
            </div>
        </div>
    );
}

export default Animations;
