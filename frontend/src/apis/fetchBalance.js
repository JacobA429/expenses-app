
import axios from 'axios'
import authToken from './config'

const fetchBalance = async () => {
    try {
        const response = await axios.get('/api/user/balance',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data['balance']
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchBalance