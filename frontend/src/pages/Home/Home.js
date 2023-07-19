import React from 'react'
import { Page, LegacyCard, Link, DataTable, FooterHelp, Text, VerticalStack, Button, HorizontalStack } from '@shopify/polaris';
import { useNavigate } from 'react-router-dom';
import { useQuery } from "react-query";
import apis from '../../apis';
import { EmptyView } from './components';

function Home() {
    const navigate = useNavigate();
    const { data: couple, isLoading: coupleLoading } = useQuery("couple", apis.fetchCouple)
    const { data: currentUser, isLoading: userLoading } = useQuery("currentUser", apis.fetchCurrentUser)
    const { data: balance, isLoading: balanceLoading } = useQuery("balance", apis.fetchBalance)

    const handleCreateExpense = () => {
        navigate('/expenses/create', { replace: false })
    }

    const signOutUser = () => {
        localStorage.removeItem("auth_token");
    }

    const allUsersLoaded = !!(couple && currentUser)

    if (coupleLoading || userLoading || balanceLoading || !allUsersLoaded) {
        return
    }
    let partnerUser = null
    if (currentUser.id == couple.user1.id) {
        partnerUser = couple.user2
    } else {
        partnerUser = couple.user1
    }

    let balanceText = null; // Initialize balanceText as null

    if (balance && balance > 0) {
        balanceText = (
            <Text variant="heading2xl" as="p" color="success">
                {partnerUser?.name} owes you ${Math.abs(balance)}!
            </Text>
        );
    } else if (balance && balance < 0) {
        balanceText = (
            <Text variant="heading2xl" as="p" color="critical">
                You need to pay {partnerUser?.name} ${Math.abs(balance)}
            </Text>
        );
    } else {
        balanceText = (
            <Text variant="heading2xl" as="p">
                Balance is $0
            </Text>
        );
    }


    const expenses = couple && couple.expenses
    const hasExpenses = expenses && expenses.length > 0 || false;
    let tableRowData = []
    let totalCount = 0
    if (hasExpenses) {
        tableRowData = expenses.map((expense) => [expense.title, new Date(expense.created_at).toDateString(), expense.paid_for_by_user.name, `$${expense.total}`])
        totalCount = expenses.reduce((accumulator, item) => accumulator + item.total, 0);
    }


    return (
        allUsersLoaded && <Page
            title="Expenses"
            subtitle={`Hello ${currentUser.name}`}
        >
            <VerticalStack gap="10">
                <HorizontalStack align='space-between'>
                    {balanceText}
                    <Button primary size="large" onClick={handleCreateExpense}>
                        Create Expense
                    </Button>
                </HorizontalStack>
                { }
                {hasExpenses ?
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
                    </LegacyCard> : <EmptyView />}
            </VerticalStack>
            <FooterHelp>
                <Button plain monochrome onClick={signOutUser}>
                    Sign Out
                </Button>
            </FooterHelp>
        </Page>
    )
}

export default Home;