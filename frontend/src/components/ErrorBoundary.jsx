import React from 'react';

/**
 * Error Boundary Component
 * Catches JavaScript errors in child components and displays a fallback UI
 */
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        this.setState({
            error: error,
            errorInfo: errorInfo
        });
    }

    handleReset = () => {
        this.setState({ hasError: false, error: null, errorInfo: null });
    };

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    padding: '2rem',
                    textAlign: 'center',
                    background: 'rgba(239, 68, 68, 0.1)',
                    borderRadius: '12px',
                    border: '1px solid #ef4444',
                    margin: '1rem'
                }}>
                    <h3 style={{ color: '#ef4444', marginBottom: '1rem' }}>
                        ⚠️ Something went wrong
                    </h3>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
                        The visualization encountered an error. This is usually temporary.
                    </p>
                    {this.state.error && (
                        <details style={{
                            textAlign: 'left',
                            marginBottom: '1rem',
                            background: 'rgba(0,0,0,0.2)',
                            padding: '0.5rem',
                            borderRadius: '4px'
                        }}>
                            <summary style={{ cursor: 'pointer', color: 'var(--text-secondary)' }}>
                                Error Details
                            </summary>
                            <pre style={{
                                fontSize: '0.75rem',
                                color: '#ef4444',
                                overflow: 'auto',
                                maxHeight: '100px'
                            }}>
                                {this.state.error.toString()}
                            </pre>
                        </details>
                    )}
                    <button
                        className="btn btn-primary"
                        onClick={this.handleReset}
                        style={{ marginRight: '0.5rem' }}
                    >
                        🔄 Try Again
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
