import axios from 'axios'
import authToken from './config'

const fetchCouple = async () => {
    try {
        const response = await axios.get('/api/couple',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.couple
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchCouple