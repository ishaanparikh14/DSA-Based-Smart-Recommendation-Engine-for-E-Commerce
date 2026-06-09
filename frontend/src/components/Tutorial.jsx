import { useState } from 'react';

const tutorialSteps = [
    {
        title: 'Welcome to DSA E-Commerce! 🎉',
        description: 'This tutorial will show you how Data Structures power every action in this app.',
        highlight: null,
    },
    {
        title: 'Shopping Cart - Doubly Linked List 🔗',
        description: 'When you ADD TO CART, we perform an INSERT operation on a Doubly Linked List. O(1) time complexity with hash map lookup!',
        operation: 'INSERT',
        dataStructure: 'Doubly Linked List',
        highlight: 'cart',
    },
    {
        title: 'Remove from Cart - DELETE Operation 🗑️',
        description: 'Clicking REMOVE performs a DELETE operation on the linked list. The node is unlinked and removed in O(1) time.',
        operation: 'DELETE',
        dataStructure: 'Doubly Linked List',
        highlight: 'cart',
    },
    {
        title: 'Product Views - Stack (PUSH) 📚',
        description: 'Every time you view a product, we PUSH it onto a Stack. Your recent views are stored in LIFO order.',
        operation: 'PUSH',
        dataStructure: 'Stack',
        highlight: 'products',
    },
    {
        title: 'Action Tracking - Queue (ENQUEUE) 🔄',
        description: 'All your actions are logged by ENQUEUE operations on a Queue. FIFO order ensures chronological tracking.',
        operation: 'ENQUEUE',
        dataStructure: 'Queue',
        highlight: 'dsa-activity',
    },
    {
        title: 'Category Matching - Trie Search 🌳',
        description: 'Recommendations use a TRIE SEARCH to match your preferred categories. Fast prefix-based filtering!',
        operation: 'TRIE SEARCH',
        dataStructure: 'Trie',
        highlight: 'recommendations',
    },
    {
        title: 'Price Filtering - BST Range Query 🔍',
        description: 'Price and inventory filters use BST RANGE QUERY operations for efficient searching.',
        operation: 'BST QUERY',
        dataStructure: 'Binary Search Tree',
        highlight: 'products',
    },
    {
        title: 'Top Recommendations - Heap Selection ⛰️',
        description: 'The best recommendations are selected using HEAP EXTRACT operations. O(n log k) efficiency!',
        operation: 'HEAP EXTRACT',
        dataStructure: 'Min/Max Heap',
        highlight: 'recommendations',
    },
    {
        title: 'Frequently Bought Together - Graph Traversal 🕸️',
        description: 'Co-occurrence analysis uses GRAPH TRAVERSAL to find products bought together.',
        operation: 'GRAPH QUERY',
        dataStructure: 'Weighted Graph',
        highlight: 'recommendations',
    },
    {
        title: 'Watch the DSA Activity Panel! 👀',
        description: 'The right panel shows REAL-TIME DSA operations. Every action you take triggers data structure operations!',
        highlight: 'dsa-activity',
    },
    {
        title: 'You\'re All Set! 🚀',
        description: 'Now you know how classical algorithms power this entire app. No ML, no AI - just pure DSA! Start shopping and watch the operations happen in real-time.',
        highlight: null,
    },
];

function Tutorial({ onComplete }) {
    const [currentStep, setCurrentStep] = useState(0);

    const handleNext = () => {
        if (currentStep < tutorialSteps.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            onComplete();
        }
    };

    const handleSkip = () => {
        onComplete();
    };

    const step = tutorialSteps[currentStep];

    return (
        <div className="tutorial-overlay">
            <div className="tutorial-modal">
                <div className="tutorial-header">
                    <h2>{step.title}</h2>
                    <button className="tutorial-close" onClick={handleSkip}>
                        ✕
                    </button>
                </div>

                <div className="tutorial-content">
                    <p>{step.description}</p>

                    {step.operation && (
                        <div className="tutorial-operation">
                            <div className="operation-badge">
                                <span className="operation-label">Operation:</span>
                                <span className="operation-value">{step.operation}</span>
                            </div>
                            <div className="ds-badge">
                                <span className="ds-label">Data Structure:</span>
                                <span className="ds-value">{step.dataStructure}</span>
                            </div>
                        </div>
                    )}

                    <div className="tutorial-progress">
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
                            ></div>
                        </div>
                        <div className="progress-text">
                            Step {currentStep + 1} of {tutorialSteps.length}
                        </div>
                    </div>
                </div>

                <div className="tutorial-footer">
                    <button className="btn btn-secondary" onClick={handleSkip}>
                        Skip Tutorial
                    </button>
                    <button className="btn btn-primary" onClick={handleNext}>
                        {currentStep < tutorialSteps.length - 1 ? 'Next' : 'Get Started!'}
                    </button>
                </div>
            </div>

            {step.highlight && (
                <div className="tutorial-highlight" data-highlight={step.highlight}></div>
            )}
        </div>
    );
}

export default Tutorial;
