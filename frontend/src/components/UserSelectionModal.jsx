import { useState } from 'react';

function UserSelectionModal({ users, onSelectUser }) {
    const [selectedUserId, setSelectedUserId] = useState('');

    const handleSelect = () => {
        const user = users.find((u) => u.id === selectedUserId);
        if (user) {
            onSelectUser(user);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal" style={{ maxWidth: '800px' }}>
                <h1 style={{ marginBottom: '1rem', textAlign: 'center' }}>
                    Welcome to DSA E-Commerce Engine
                </h1>

                <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginBottom: '2rem' }}>
                    Select a user to experience personalized recommendations
                </div>

                <div
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
                        gap: '1rem',
                        marginBottom: '2rem',
                    }}
                >
                    {users.map((user) => (
                        <div
                            key={user.id}
                            onClick={() => setSelectedUserId(user.id)}
                            style={{
                                padding: '1rem',
                                background: selectedUserId === user.id ? 'var(--primary)' : 'var(--bg-secondary)',
                                border: `2px solid ${selectedUserId === user.id ? 'var(--primary)' : 'var(--border-color)'}`,
                                borderRadius: '8px',
                                cursor: 'pointer',
                                transition: 'var(--transition)',
                                textAlign: 'center',
                            }}
                        >
                            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                                👤
                            </div>
                            <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                                {user.name}
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                {user.id}
                            </div>
                            {user.preferred_categories && user.preferred_categories.length > 0 && (
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                    {user.preferred_categories.slice(0, 2).join(', ')}
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                <button
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                    onClick={handleSelect}
                    disabled={!selectedUserId}
                >
                    Continue as {users.find((u) => u.id === selectedUserId)?.name || 'User'}
                </button>

                <div
                    style={{
                        marginTop: '2rem',
                        padding: '1rem',
                        background: 'var(--bg-secondary)',
                        borderRadius: '8px',
                        fontSize: '0.85rem',
                        color: 'var(--text-muted)',
                    }}
                >
                    <strong>🎓 Academic Project Features:</strong>
                    <ul style={{ marginTop: '0.5rem', marginLeft: '1.5rem' }}>
                        <li>8 Custom Data Structures (NO external libraries)</li>
                        <li>Category-First Recommendation Algorithm</li>
                        <li>100% Explainable - NO Machine Learning</li>
                        <li>Real-time DSA Operation Visualization</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default UserSelectionModal;
