import { LegacyCard, EmptyState } from '@shopify/polaris';

function EmptyView() {
    return (<LegacyCard sectioned>
        <EmptyState
            heading="No Expenses yet!"
            image="https://cdn.shopify.com/s/files/1/0262/4071/2726/files/emptystate-files.png"
        >
            <p>Create an expense to get started</p>
        </EmptyState>
    </LegacyCard>)
}

export default EmptyView;