import React, { useState } from 'react'
import { FormLayout, Page, TextField, Button, Form } from '@shopify/polaris';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

function Signup() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState();

    const navigate = useNavigate();

    const handleEmailChange = (event) => {
        setEmail(event)
    }

    const handleNameChange = (event) => {
        setName(event)
    }

    const handlePasswordChange = (event) => {
        setPassword(event)
    }
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