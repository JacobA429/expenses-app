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
import { QueryClient, QueryClientProvider } from 'react-query'
import AuthenticatedRoute from './AuthenticatedRoute';

const root = ReactDOM.createRoot(document.getElementById('root'));
const queryClient = new QueryClient()

root.render(
  <AppProvider>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route index element={<App />} />
          <Route path="signup" element={<Signup />} />
          <Route path="invite" element={<InviteLink />} />
          <Route path="join/:token" element={<PartnerSignup />} />
          <Route path="home" element={<AuthenticatedRoute>
            <Home />
          </AuthenticatedRoute>} />
          <Route path='expenses/create' element={<AuthenticatedRoute>
            <ExpenseForm />
          </AuthenticatedRoute>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </AppProvider>,
);
