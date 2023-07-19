import axios from 'axios'
import authToken from './config'

const createExpense = (data) => {
    axios.post('/api/expenses/create', { ...data }, { headers: { 'Authorization': `Bearer ${authToken}` } }).then(response => {
        return response.data
    }).catch(error => {
        console.log(error)
    })
}

export default createExpense