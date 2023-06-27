import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Signup } from './pages/Signup';
import { AppProvider } from '@shopify/polaris'
import '@shopify/polaris/build/esm/styles.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { InviteLink } from './pages/InviteLink';
import { PartnerSignup } from './pages/PartnerSignup';
import { ExpenseForm } from './pages/ExpenseForm';
import { Home } from './pages/Home';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AppProvider>
    <BrowserRouter>
      <Routes>
        <Route index element={<App />} />
        <Route path="signup" element={<Signup />} />
        <Route path="invite" element={<InviteLink />} />
        <Route path="join/:token" element={<PartnerSignup />} />
        <Route path="home" element={<Home />} />
        <Route path='expenses/create' element={<ExpenseForm />} />
      </Routes>
    </BrowserRouter>
  </AppProvider>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
