import React, { useEffect, useState } from 'react'
import { FormLayout, Page, TextField, Button, Form, Text } from '@shopify/polaris';
import axios from 'axios'
import { useParams } from 'react-router-dom';

function PartnerSignup() {

    const { token } = useParams();
    const [user1, setUser1] = useState()
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState();


    const handleEmailChange = (event) => {
        setEmail(event)
    }

    const handleNameChange = (event) => {
        setName(event)
    }

    const handlePasswordChange = (event) => {
        setPassword(event)
    }

    useEffect(() => {
        // Function to call the API
        const fetchData = async () => {
            try {
                const response = await axios.get(`/api/join/${token}`)
                setUser1(response.data.user1)
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [token]);

    const handleSubmit = () => {
        axios.post('/auth/signup', { 'email': email, 'password': password, 'name': name }).then(response => {
            axios.post('/api/create_couple', { 'user1_id': user1.id, 'user2_id': response.data.id }).then(response => {
                console.log(response.data)
                axios.post('/auth/login', { 'email': email, 'password': password }).then(response => {
                    localStorage.setItem('auth_token', response.data.token)
                }).catch(error => {
                    console.log(error)
                })
            }).catch(error => {
                console.log(error)
            })
        }).catch(error => {
            console.log(error)
        })
    }
    return (
        <Page title='Sign Up'>
            <Form onSubmit={handleSubmit}>
                <FormLayout>
                    <TextField
                        value={name}
                        label="Name"
                        onChange={handleNameChange}
                    />
                    <TextField
                        value={email}
                        type="email"
                        label="Email"
                        onChange={handleEmailChange}
                        autoComplete="email"
                    />

                    <TextField
                        value={password}
                        label="Password"
                        type='password'
                        onChange={handlePasswordChange} autoComplete="off"
                    />
                    <Button submit size='large' primary>Submit</Button>;
                </FormLayout>
            </Form>
            <Text variant="heading2xl" as="h3">
                {user1 && <p>{user1.name} invited you! Fill out details above to get started!</p>}
            </Text>
        </Page>
    )
}

export default PartnerSignup;