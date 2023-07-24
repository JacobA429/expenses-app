import React, { useEffect, useState } from 'react'
import { FormLayout, Page, TextField, Button, Form, Text } from '@shopify/polaris';
import axios from 'axios'
import { useParams } from 'react-router-dom';
import { faker } from '@faker-js/faker';
import { useNavigate } from 'react-router-dom';
import authToken from '../../apis/config';


function PartnerSignup() {
    const navigate = useNavigate();
    const { token } = useParams();
    const [user1, setUser1] = useState()
    const [name, setName] = useState(faker.person.firstName());
    const [email, setEmail] = useState(`${name}@email.com`);
    const [password, setPassword] = useState('password');


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
                console.log(response.data.user1)
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [token]);

    const handleSubmit = () => {
        axios.post('/auth/signup', { 'email': email, 'password': password, 'name': name }).then(response => {
            console.log(response.data)
            axios.post('/api/couple/create', { 'user1_id': user1.id, 'user2_id': response.data.id }).then(response => {
                axios.post('/auth/login', { 'email': email, 'password': password }).then(response => {
                    localStorage.setItem('auth_token', response.data.token)
                    navigate('/home', { replace: false })
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