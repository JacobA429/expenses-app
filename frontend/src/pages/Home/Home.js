import React, { useEffect, useState } from 'react'
import { Page } from '@shopify/polaris';
import axios from 'axios'

function Home() {

    return (
        <Page>
            <h1>{partnerLink}</h1>
        </Page>
    )
}

export default Home;