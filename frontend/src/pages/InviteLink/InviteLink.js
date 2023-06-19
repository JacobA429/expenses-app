import React, { useEffect, useState } from 'react'
import { FormLayout, Page, TextField, Button, Form } from '@shopify/polaris';
import axios from 'axios'

function InviteLink() {

    const [partnerLink, setPartnerLink] = useState('');
    useEffect(() => {
        // Function to call the API
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
    // const handleSubmit = () => {
    //     axios.post('/auth/signup', { 'email': email, 'password': password, 'name': name }).then(response => {
    //         axios.post('/auth/login', { 'email': email, 'password': password }).then(response => {
    //             console.log("SUCCESS", response)
    //             localStorage.setItem('auth_token', response.data.token)

    //         }).catch(error => {
    //             console.log(error)
    //         })
    //     }).catch(error => {
    //         console.log(error)
    //     })
    // }
    // HandleChange method to update the states
    return (
        <Page title='Sign Up'>
            <h1>{partnerLink}</h1>
        </Page>
    )
}

export default InviteLink;