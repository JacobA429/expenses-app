import React from 'react'
import { Navigate } from 'react-router-dom'

const AuthenticatedRoute = ({ children }) => {
    const authToken = localStorage.getItem('auth_token')

    return authToken ? children : <Navigate to='/signup' />
}

export default AuthenticatedRoute