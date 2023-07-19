import React, { useEffect, useState } from 'react'
import { Page } from '@shopify/polaris';
import axios from 'axios'

function InviteLink() {

    const [partnerLink, setPartnerLink] = useState('');
    useEffect(() => {
        const fetchData = async () => {
            try {
                const auth_token = localStorage.getItem('auth_token')
                if (auth_token) {
                    const response = await axios.get('/api/partner_link',
                        { headers: { 'Authorization': `Bearer ${auth_token}` } })
                    setPartnerLink(response.data.link)

                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        // Call the API when the component mounts
        fetchData();
    }, []);

    return (
        <Page title='Sign Up'>
            <h1>{partnerLink}</h1>
        </Page>
    )
}

export default InviteLink;