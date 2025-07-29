import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home'
import Results from './pages/Results'
import Auth from './pages/Auth'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing auth token on app load
    const token = localStorage.getItem('authToken')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      setIsAuthenticated(true)
      setUser(JSON.parse(userData))
    }
    
    setLoading(false)
  }, [])

  const handleLogin = (_token: string, userData: any) => {
    setIsAuthenticated(true)
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>RedditHarbor UI</h1>
          {isAuthenticated && (
            <div className="user-info">
              <span>Welcome, {user?.username || 'User'}!</span>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          )}
        </header>
        <main>
          <Routes>
            <Route 
              path="/" 
              element={
                isAuthenticated ? <Home /> : <Navigate to="/auth" replace />
              } 
            />
            <Route 
              path="/results/:jobId" 
              element={
                isAuthenticated ? <Results /> : <Navigate to="/auth" replace />
              } 
            />
            <Route 
              path="/auth" 
              element={
                isAuthenticated ? <Navigate to="/" replace /> : <Auth onLogin={handleLogin} />
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App 