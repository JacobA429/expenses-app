import React, { useEffect, useState } from 'react'
import { Page, LegacyCard, DataTable, EmptyState, Text, VerticalStack } from '@shopify/polaris';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';


function Home() {
    const navigate = useNavigate();
    const [expenses, setExpenses] = useState([])
    const [balance, setBalance] = useState(0)

    const handleCreateExpense = () => {
        navigate('/expenses/create', { replace: false })
    }

    let tableRowData = []
    let totalCount = 0
    if (expenses) {
        tableRowData = expenses.map((expense) => [expense.title, new Date(expense.created_at).toDateString(), expense.paid_for_by_user.name, expense.total])
        totalCount = expenses.reduce((accumulator, item) => accumulator + item.total, 0);
    }

    useEffect(() => {
        const authToken = localStorage.getItem('auth_token')

        const fetchExpenses = async () => {
            try {

                const fetchData = async () => {
                    try {
                        if (authToken) {
                            const expensesResponse = await axios.get('/api/expenses/all',
                                { headers: { 'Authorization': `Bearer ${authToken}` } })
                            const apiExpenses = expensesResponse.data.expenses
                            setExpenses(apiExpenses)

                            const balanceResponse = await axios.get('/api/user/balance',
                                { headers: { 'Authorization': `Bearer ${authToken}` } })
                            setBalance(balanceResponse.data['balance'])

                        }
                    } catch (error) {
                        console.error('Error fetching data:', error);
                    }
                };

                // Call the API when the component mounts
                fetchData();
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchExpenses();
    }, []);

    const emptyState = <LegacyCard sectioned>
        <EmptyState
            heading="No Expenses to report"
            image="https://cdn.shopify.com/s/files/1/0262/4071/2726/files/emptystate-files.png"
        >
            <p>Create an expense to get started</p>
        </EmptyState>
    </LegacyCard>

    const balanceOwedText = balance && <Text variant="heading2xl" as="p" color="success">
        You are owed ${balance}!
    </Text>

    const balanceOweText = balance && <Text variant="heading2xl" as="p" color="critical">
        You are owed ${balance}!
    </Text>


    return (
        <>
            <Page
                title="Expenses"
                primaryAction={{ content: 'Create Expense', onAction: handleCreateExpense }}
            >
                <VerticalStack gap="10">
                    {balance > 0 ? balanceOwedText : balanceOweText}
                    { }
                    {expenses.length > 0 ?
                        <LegacyCard>
                            <DataTable
                                columnContentTypes={[
                                    'text',
                                    'numeric',
                                    'numeric',
                                    'numeric',
                                ]}
                                headings={[
                                    'Title',
                                    'Date created',
                                    'Paid By',
                                    'Total Cost',
                                ]}
                                rows={tableRowData}
                                totalsName={'Total Cost'}
                                totals={['', '', '', "$" + totalCount]}
                                showTotalsInFooter
                            />
                        </LegacyCard> : emptyState}
                </VerticalStack>
            </Page>
        </>
    )
}

export default Home;