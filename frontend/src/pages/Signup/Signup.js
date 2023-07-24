import React, { useState, useCallback } from 'react'
import { FormLayout, Page, TextField, Button, Form } from '@shopify/polaris';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import { faker } from '@faker-js/faker';


function Signup() {
    const [name, setName] = useState(faker.person.firstName());
    const [email, setEmail] = useState(`${name}@email.com`);
    const [password, setPassword] = useState('password');

    const navigate = useNavigate();

    const handleEmailChange = useCallback((value) => setEmail(value), []);
    const handleNameChange = useCallback((value) => setName(value), []);
    const handlePasswordChange = useCallback((value) => setPassword(value), []);

    const handleSubmit = () => {
        axios.post('/auth/signup', { 'email': email, 'password': password, 'name': name }).then(response => {
            axios.post('/auth/login', { 'email': email, 'password': password }).then(response => {
                localStorage.setItem('auth_token', response.data.token)
                navigate('/invite', { replace: true })
            }).catch(error => {
                console.log(error)
            })
        }).catch(error => {
            console.log(error)
        })
    }
    // HandleChange method to update the states
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
        </Page>
    )
}

export default Signup;