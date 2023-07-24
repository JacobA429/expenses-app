import axios from 'axios'

const fetchCurrentUser = async () => {
    try {
        const authToken = localStorage.getItem('auth_token')
        const response = await axios.get('/api/user/current',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.user
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchCurrentUser