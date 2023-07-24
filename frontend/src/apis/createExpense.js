import axios from 'axios'

const createExpense = (data) => {
    const authToken = localStorage.getItem('auth_token')
    axios.post('/api/expenses/create', { ...data }, { headers: { 'Authorization': `Bearer ${authToken}` } }).then(response => {
        return response.data
    }).catch(error => {
        console.log(error)
    })
}

export default createExpense