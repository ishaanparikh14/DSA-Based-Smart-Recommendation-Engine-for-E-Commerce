import { useState, useEffect } from 'react';
import { getDSAActivity } from '../api';

function DSAActivityPanel() {
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadActivities();
        // Poll for new activities every 2 seconds
        const interval = setInterval(loadActivities, 2000);
        return () => clearInterval(interval);
    }, []);

    const loadActivities = async () => {
        try {
            const response = await getDSAActivity(20);
            setActivities(response.data.activity);
            setLoading(false);
        } catch (error) {
            console.error('Error loading DSA activity:', error);
            setLoading(false);
        }
    };

    const getOperationColor = (operation) => {
        const colors = {
            PUSH: '#10b981',
            POP: '#f59e0b',
            INSERT: '#6366f1',
            DELETE: '#ef4444',
            ENQUEUE: '#8b5cf6',
            DEQUEUE: '#ec4899',
            RECOMMEND: '#06b6d4',
            GRAPH_QUERY: '#14b8a6',
            PRICE_CALC: '#f59e0b',
        };
        return colors[operation] || '#94a3b8';
    };

    if (loading) {
        return (
            <div className="dsa-activity">
                <div className="spinner" style={{ width: '30px', height: '30px' }}></div>
            </div>
        );
    }

    return (
        <div className="dsa-activity">
            <div style={{ marginBottom: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                Real-time Data Structure Operations
            </div>

            {activities.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                    No recent activity
                </div>
            ) : (
                activities.map((activity, index) => (
                    <div
                        key={activity.timestamp || index}
                        className="dsa-activity-item"
                        style={{
                            borderLeftColor: getOperationColor(activity.operation),
                        }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                            <span
                                className="dsa-operation"
                                style={{ color: getOperationColor(activity.operation) }}
                            >
                                {activity.operation}
                            </span>
                            <span className="dsa-structure">
                                {activity.data_structure}
                            </span>
                        </div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                            {activity.details}
                        </div>
                    </div>
                ))
            )}

        </div>
    );
}

export default DSAActivityPanel;
