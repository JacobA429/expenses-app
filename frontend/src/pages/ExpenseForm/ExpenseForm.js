import React, { useState, useCallback } from 'react'
import { FormLayout, Page, TextField, Button, Form, DatePicker, Text, ChoiceList, Frame, Loading, Toast } from '@shopify/polaris';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from "react-query";
import apis from '../../apis';

function ExpenseForm() {
    const { data: couple } = useQuery("couple", apis.fetchCouple)
    const { mutate } = useMutation(apis.createExpense, {
        onSuccess: data => {
            toggleExpenseCreated()
            navigate('/home', { replace: true })
        },

        onError: () => {
            alert("There was an error")
        }
    })
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

    const handleTitleChange = useCallback((value) => setTitle(value), []);
    const handleTotalChange = useCallback((value) => setTotal(value), []);

    const handleSubmit = () => {
        const created_at = selectedDates.start.toDateString()
        const paid_by_user_id = selectedUser[0]
        mutate({ title, total, created_at, paid_by_user_id })
    }

    const [selectedUser, setSelectedUser] = useState('hidden');

    const handleChange = useCallback((value) => setSelectedUser(value), []);
    // HandleChange method to update the states

    const toastMarkup = expenseCreated ? (
        <Toast content="Expense Created!" onDismiss={toggleExpenseCreated} />
    ) : null;

    let userNameChoices = []
    if (couple) {
        userNameChoices = [couple.user1, couple.user2].map((u) => { return { label: u.name, value: u.id } })
    }

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
                        {couple && <ChoiceList
                            allowMultiple={false}
                            title="Select who paid"
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

    return contentRender
}

export default ExpenseForm;