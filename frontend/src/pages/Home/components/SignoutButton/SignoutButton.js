import { Button } from '@shopify/polaris';
import { useNavigate } from 'react-router-dom';

function SignoutButton() {
    const navigate = useNavigate();

    const signOutUser = () => {
        localStorage.removeItem("auth_token");
        navigate('/signup', { replace: false })
    }

    return (<Button plain monochrome onClick={signOutUser}>
        Sign Out
    </Button>)
}

export default SignoutButton;