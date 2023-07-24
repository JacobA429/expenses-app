import axios from 'axios'

const fetchCouple = async () => {
    try {
        const authToken = localStorage.getItem('auth_token')
        const response = await axios.get('/api/couple/current',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.couple
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchCouple