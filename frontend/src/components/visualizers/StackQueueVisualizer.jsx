import { useState, useEffect } from 'react';
import api from '../../api';

function StackQueueVisualizer({ currentUser }) {
    const [stack, setStack] = useState([]);
    const [queue, setQueue] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (currentUser) {
            refreshData();
        }
    }, [currentUser]);

    const refreshData = async () => {
        try {
            const stackRes = await api.get(`/recent-views/${currentUser.id}`);
            const queueRes = await api.get(`/session-queue/${currentUser.id}`);
            setStack(stackRes.data.views || []);
            setQueue(queueRes.data.queue || []);
        } catch (err) {
            console.error(err);
        }
    };

    const handlePop = async () => {
        try {
            await api.post(`/view/${currentUser.id}/pop`);
            refreshData();
        } catch (err) {
            console.error(err);
        }
    };

    const handleDequeue = async () => {
        try {
            await api.post(`/session-queue/${currentUser.id}/dequeue`);
            refreshData();
        } catch (err) {
            console.error(err);
        }
    };

    if (!currentUser) return <div>Please log in to view User Data Structures.</div>;

    return (
        <div className="visualizer-container" style={{ display: 'flex', gap: '20px' }}>
            {/* Stack Section */}
            <div style={{ flex: 1, border: '1px solid #333', padding: '15px', borderRadius: '8px' }}>
                <h3>Stack (LIFO) - Recent Views</h3>
                <button className="btn btn-secondary" onClick={handlePop} disabled={stack.length === 0} style={{ width: '100%', marginBottom: '10px' }}>
                    ↩️ POP (Undo View)
                </button>
                <div className="structure-view">
                    {stack.slice(0, 10).map((item, i) => (
                        <div key={i} style={{
                            padding: '10px', margin: '5px 0',
                            background: '#2a2a2a', borderLeft: '3px solid #00cc66',
                            display: 'flex', justifyContent: 'space-between'
                        }}>
                            <span>{item.product ? item.product.name : `Product ${item.product_id}`}</span>
                            <small>Top - {i}</small>
                        </div>
                    ))}
                </div>
            </div>

            {/* Queue Section */}
            <div style={{ flex: 1, border: '1px solid #333', padding: '15px', borderRadius: '8px' }}>
                <h3>Queue (FIFO) - Session Actions</h3>
                <button className="btn btn-secondary" onClick={handleDequeue} disabled={queue.length === 0} style={{ width: '100%', marginBottom: '10px' }}>
                    📤 DEQUEUE (Process Item)
                </button>
                <div className="structure-view">
                    {queue.slice(0, 10).map((item, i) => (
                        <div key={i} style={{
                            padding: '10px', margin: '5px 0',
                            background: '#2a2a2a', borderLeft: '3px solid #ff0055',
                            display: 'flex', justifyContent: 'space-between'
                        }}>
                            <span>{item.action === 'view_product' ? 'View' : 'Cart Add'}</span>
                            <small>Front + {i}</small>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default StackQueueVisualizer;
