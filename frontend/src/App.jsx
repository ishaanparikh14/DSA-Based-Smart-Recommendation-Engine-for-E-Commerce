import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import './App.css';
import LandingPage from './components/LandingPage';
import ProductGrid from './components/ProductGrid';
import Cart from './components/Cart';
import RecommendationPanel from './components/RecommendationPanel';
import UserSelectionModal from './components/UserSelectionModal';
import DSAActivityPanel from './components/DSAActivityPanel';
import PurchaseHistory from './components/PurchaseHistory';
import Tutorial from './components/Tutorial';
import LiveDSAMonitor from './components/LiveDSAMonitor';
import DSAApplications from './components/DSAApplications';
import Animations from './components/Animations';
import ProductSimilarityGraph from './components/visualizers/ProductSimilarityGraph';
import { getUsers } from './api';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [showUserModal, setShowUserModal] = useState(true);
  const [cartCount, setCartCount] = useState(0);
  const [showTutorial, setShowTutorial] = useState(false);
  const [tutorialCompleted, setTutorialCompleted] = useState(false);

  useEffect(() => {
    // Load users
    getUsers()
      .then((response) => {
        setUsers(response.data);
      })
      .catch((error) => {
        console.error('Error loading users:', error);
      });
  }, []);

  const handleUserSelect = (user) => {
    setCurrentUser(user);
    setShowUserModal(false);
    setTutorialCompleted(false);
    // Always show tutorial for new user selection
    setShowTutorial(true);
  };

  const handleUserSwitch = (e) => {
    const userId = e.target.value;
    const user = users.find((u) => u.id === userId);
    if (user) {
      setCurrentUser(user);
    }
  };

  const handleTutorialComplete = () => {
    setShowTutorial(false);
    setTutorialCompleted(true);
    // Don't redirect, just close tutorial - user is already on home page
  };

  if (!currentUser && showUserModal && !tutorialCompleted) {
    return (
      <UserSelectionModal
        users={users}
        onSelectUser={handleUserSelect}
      />
    );
  }

  return (
    <Router>
      <div className="app">
        <Header
          currentUser={currentUser}
          users={users}
          onUserSwitch={handleUserSwitch}
          cartCount={cartCount}
          onShowTutorial={() => setShowTutorial(true)}
        />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<LandingPage currentUser={currentUser} />} />
            <Route
              path="/products"
              element={
                <ProductsPage
                  currentUser={currentUser}
                  setCartCount={setCartCount}
                />
              }
            />
            <Route
              path="/cart"
              element={
                <Cart
                  currentUser={currentUser}
                  setCartCount={setCartCount}
                />
              }
            />
            <Route
              path="/recommendations"
              element={
                <RecommendationPanel
                  currentUser={currentUser}
                  setCartCount={setCartCount}
                />
              }
            />
            <Route
              path="/dsa-applications"
              element={
                <DSAApplications
                  currentUser={currentUser}
                />
              }
            />
            <Route
              path="/animations"
              element={
                <Animations
                  currentUser={currentUser}
                />
              }
            />
            <Route
              path="/history"
              element={
                <PurchaseHistory
                  currentUser={currentUser}
                  users={users}
                  setCurrentUser={setCurrentUser}
                />
              }
            />
            <Route
              path="/graph-repre"
              element={
                <ProductSimilarityGraph
                  currentUser={currentUser}
                />
              }
            />
          </Routes>
        </main>

        {showTutorial && (
          <Tutorial onComplete={handleTutorialComplete} />
        )}
        <LiveDSAMonitor />
      </div>
    </Router>
  );
}

function Header({ currentUser, users, onUserSwitch, cartCount, onShowTutorial }) {
  const location = useLocation();

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          🧠 DSA E-Commerce
        </div>

        <nav className="nav">
          <Link
            to="/"
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link
            to="/products"
            className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}
          >
            Products
          </Link>
          <Link
            to="/recommendations"
            className={`nav-link ${location.pathname === '/recommendations' ? 'active' : ''}`}
          >
            Recommendations
          </Link>
          <Link
            to="/dsa-applications"
            className={`nav-link ${location.pathname === '/dsa-applications' ? 'active' : ''}`}
          >
            🧠 DSA Applications
          </Link>
          <Link
            to="/animations"
            className={`nav-link ${location.pathname === '/animations' ? 'active' : ''}`}
            style={{ color: '#ff0055', fontWeight: 'bold' }}
          >
            ✨ Animations
          </Link>
          <Link
            to="/history"
            className={`nav-link ${location.pathname === '/history' ? 'active' : ''}`}
          >
            Purchase History
          </Link>
          <Link
            to="/graph-repre"
            className={`nav-link ${location.pathname === '/graph-repre' ? 'active' : ''}`}
            style={{ color: '#00ffff', fontWeight: 'bold' }}
          >
            🕸️ Graph Repre
          </Link>
          <Link
            to="/cart"
            className={`nav-link ${location.pathname === '/cart' ? 'active' : ''}`}
          >
            Cart {cartCount > 0 && `(${cartCount})`}
          </Link>
        </nav>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            className="btn btn-secondary"
            onClick={onShowTutorial}
            style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
          >
            📚 Tutorial
          </button>

          <div className="user-switcher">
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              User:
            </span>
            <select value={currentUser?.id || ''} onChange={onUserSwitch}>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name} ({user.id})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </header>
  );
}

function ProductsPage({ currentUser, setCartCount }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '2rem' }}>
      <div>
        <h1 style={{ marginBottom: '1rem' }}>Browse Products</h1>
        <ProductGrid currentUser={currentUser} setCartCount={setCartCount} />
      </div>
      <div>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.2rem' }}>DSA Operations</h2>
        <DSAActivityPanel />
      </div>
    </div>
  );
}

export default App;
