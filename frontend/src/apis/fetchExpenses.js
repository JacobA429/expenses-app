import axios from 'axios'
import authToken from './config'

const fetchExpenses = async () => {
    try {
        const response = await axios.get('/api/expenses/all',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.expenses
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchExpenses