import axios from 'axios'
import authToken from './config'

const fetchCurrentUser = async () => {
    try {
        const response = await axios.get('/api/user/current',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.user
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchCurrentUser