import { useState, useEffect, useRef } from 'react';
import { getDSAActivity } from '../api';

function LiveDSAMonitor() {
    const [latestActivity, setLatestActivity] = useState(null);
    const [previousActivity, setPreviousActivity] = useState(null);
    const [isExpanded, setIsExpanded] = useState(true);

    // Polling refs to avoid closure staleness if needed, though simple interval is fine here
    // We poll every 500ms for "real-time" feel
    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                // Fetch last 1 item primarily
                const response = await getDSAActivity(1);
                if (response.data && response.data.length > 0) {
                    const newest = response.data[response.data.length - 1]; // Backend appends, so last is newest

                    setLatestActivity(prev => {
                        // Only update if timestamp or details changed
                        if (!prev || prev.timestamp !== newest.timestamp) {
                            setPreviousActivity(prev); // Shift current to previous
                            return newest;
                        }
                        return prev;
                    });
                }
            } catch (error) {
                // Silent fail for polling
            }
        }, 800);

        return () => clearInterval(interval);
    }, []);

    if (!latestActivity) return null;

    return (
        <div className={`live-dsa-monitor ${isExpanded ? 'expanded' : 'collapsed'}`}>
            <div className="monitor-header">
                <div className="monitor-title">
                    <span className="live-dot"></span>
                    Live Mainframe Operations
                </div>
                <button
                    className="monitor-toggle"
                    onClick={() => setIsExpanded(!isExpanded)}
                >
                    {isExpanded ? '▼' : '▲'}
                </button>
            </div>

            {isExpanded && (
                <div className="monitor-content">
                    <div className="monitor-row latest">
                        <div className="monitor-cell op-type">
                            <span className="code-font">{latestActivity.operation}</span>
                        </div>
                        <div className="monitor-cell op-struct">
                            <span className="badge">{latestActivity.data_structure}</span>
                        </div>
                        <div className="monitor-cell op-details">
                            {latestActivity.details}
                        </div>
                        <div className="monitor-cell op-time">
                            {new Date(latestActivity.timestamp).toLocaleTimeString().split(' ')[0]}
                        </div>
                    </div>

                    {previousActivity && (
                        <div className="monitor-row previous">
                            <div className="monitor-cell op-type">
                                <span className="code-font muted">{previousActivity.operation}</span>
                            </div>
                            <div className="monitor-cell op-struct">
                                <span className="badge muted">{previousActivity.data_structure}</span>
                            </div>
                            <div className="monitor-cell op-details muted">
                                {previousActivity.details}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default LiveDSAMonitor;
