import React, { useState, useCallback, useEffect } from 'react'
import { FormLayout, Page, TextField, Button, Form, DatePicker, Text, ChoiceList, Frame, Loading, Toast } from '@shopify/polaris';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

function ExpenseForm() {
    const [users, setUsers] = useState(null)
    const today = new Date()
    const [title, setTitle] = useState("");
    const [total, setTotal] = useState(0.0);
    const [{ month, year }, setDate] = useState({ month: today.getMonth(), year: today.getFullYear() });
    const [selectedDates, setSelectedDates] = useState({
        start: today,
        end: today,
    });

    const [expenseCreated, setExpenseCreated] = useState(false);

    const toggleExpenseCreated = useCallback(() => setExpenseCreated((expenseCreated) => !expenseCreated), []);

    const handleMonthChange = useCallback(
        (month, year) => setDate({ month, year }),
        [],
    );

    const navigate = useNavigate();
    const [authToken, setAuthToken] = useState('');
    const handleTitleChange = useCallback((value) => setTitle(value), []);
    const handleTotalChange = useCallback((value) => setTotal(value), []);

    useEffect(() => {
        setAuthToken(localStorage.getItem('auth_token'))
        const fetchCouple = async () => {
            try {

                const fetchData = async () => {
                    try {
                        if (authToken) {
                            const response = await axios.get('/api/couple',
                                { headers: { 'Authorization': `Bearer ${authToken}` } })
                            const couple = response.data.couple
                            setUsers([couple.user1, couple.user2])
                        }
                    } catch (error) {
                        console.error('Error fetching data:', error);
                    }
                };

                // Call the API when the component mounts
                fetchData();
            } catch (error) {
                // Handle any network or other errors
                console.error('Error:', error);
            }
        };

        fetchCouple();
    }, []);

    const handleSubmit = () => {
        axios.post('/api/expenses/create', {
            'title': title,
            'total': total,
            'created_at': selectedDates.start.toDateString(),
            'paid_by_user_id': selectedUser[0]
        }, { headers: { 'Authorization': `Bearer ${authToken}` } }).then(response => {
            toggleExpenseCreated()
            navigate('/home', { replace: true })
        }).catch(error => {
            console.log(error)
        })
    }

    const [selectedUser, setSelectedUser] = useState('hidden');

    const handleChange = useCallback((value) => setSelectedUser(value), []);
    // HandleChange method to update the states

    const toastMarkup = expenseCreated ? (
        <Toast content="Expense Created!" onDismiss={toggleExpenseCreated} />
    ) : null;

    let userNameChoices = []
    if (users) {
        userNameChoices = users.map((u) => { return { label: u.name, value: u.id } })
    }

    const loadingIndicationRender = <div style={{ height: '100px' }}>
        <Frame>
            <Loading />
        </Frame>
    </div>

    const contentRender =
        <Frame>
            <Page title='New Expense'>
                <Form onSubmit={handleSubmit}>
                    <FormLayout>
                        <TextField
                            value={title}
                            label="Title"
                            onChange={handleTitleChange}
                        />
                        <TextField
                            value={total}
                            type="number"
                            label="Total"
                            onChange={handleTotalChange}
                            autoComplete="off"
                        />
                        {users && <ChoiceList
                            allowMultiple={false}
                            title="Company name"
                            choices={userNameChoices}
                            selected={selectedUser}
                            onChange={handleChange}
                        />}
                        <Text variant="bodyMd" as="p">
                            Date of Expense: {selectedDates.start.toDateString()}
                        </Text>
                        <DatePicker
                            month={month}
                            year={year}
                            onChange={setSelectedDates}
                            onMonthChange={handleMonthChange}
                            selected={selectedDates}
                            allowRange={false}
                        />
                        <Button submit size='large' primary>Create</Button>;
                    </FormLayout>
                </Form>
                {toastMarkup}
            </Page>
        </Frame>

    return users ? contentRender : loadingIndicationRender
}

export default ExpenseForm;