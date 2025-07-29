import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import LoginForm from '../components/LoginForm'
import RegisterForm from '../components/RegisterForm'
import './Auth.css'

interface AuthProps {
  onLogin: (token: string, user: any) => void
}

const Auth: React.FC<AuthProps> = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true)
  const navigate = useNavigate()

  const handleLogin = (token: string, user: any) => {
    // Store token in localStorage
    localStorage.setItem('authToken', token)
    localStorage.setItem('user', JSON.stringify(user))
    
    // Call parent onLogin function
    onLogin(token, user)
    
    // Navigate to home
    navigate('/')
  }

  const handleRegister = (_user: any) => {
    // After successful registration, switch to login
    setIsLogin(true)
  }

  const switchToLogin = () => setIsLogin(true)
  const switchToRegister = () => setIsLogin(false)

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>RedditHarbor UI</h1>
          <p>Sign in to manage your Reddit data collections</p>
        </div>
        
        {isLogin ? (
          <LoginForm 
            onLogin={handleLogin}
            onSwitchToRegister={switchToRegister}
          />
        ) : (
          <RegisterForm 
            onRegister={handleRegister}
            onSwitchToLogin={switchToLogin}
          />
        )}
      </div>
    </div>
  )
}

export default Auth 