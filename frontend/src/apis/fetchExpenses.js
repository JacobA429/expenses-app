import axios from 'axios'

const fetchExpenses = async () => {
    try {
        const authToken = localStorage.getItem('auth_token')
        const response = await axios.get('/api/expenses/all',
            { headers: { 'Authorization': `Bearer ${authToken}` } })
        return response.data.expenses
    } catch (error) {
        // Handle any network or other errors

    }
}

export default fetchExpenses