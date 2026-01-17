'use client'
import { useState, useRef } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'

import '@/css/pages/integrations.css'


const integrations = [
    {
        img:'/reamaze.svg',
        description: 'Easily view invoice data for your customers in Re:amaze',
        buttonText: 'Connect Re:amaze'
    },
    {
        img: '/slack.svg',
        description: 'Connect to your Slack Team and get notified when a new conversation or message comes in',
        buttonText: 'Connect Slack'
    },
    {
        img: '/stripe.svg',
        description: 'Support and billing on steroids. Process refunds, chargebacks, subscriptions and view customer charges related to conversation',
        buttonText: 'Connect Stripe'
    },
    {
        img: '/upscope.svg',
        description: 'Upscope integration will allow you to screenshare/co-browse with customers during your conversation',
        buttonText: 'Connect Upscope'
    },
    {
        img: '/paypal.svg',
        description: 'Connect to PayPal to view all the transaction details of customers',
        buttonText: 'Connect PayPal'
    },
    {
        img: '/recharge.svg',
        description: 'View Recharge subscriptions associated with your customers',
        buttonText: 'Connect ReCharge'
    },
    {
        img: '/klaviyo.svg',
        description: 'Easily view email list and campaign data for your customers in Klaviyo',
        buttonText: 'Connect Klaviyo'
    },
    {
        img: '/zapier.svg',
        description: 'Integrate Re:amaze with dozens of third party applications through Zapier',
        buttonText: 'Connect Zapier'
    },
]

export default function Integrations() {

    return <div className='page-container'>
        <>
            <div className='left-container'>
                <Menubar
                />
            </div>
            <div className='main-content'>
                <Header
                    title='Integrations'
                />
                <div className='main-content-body'>

                    <div className='integration-wrapper'>
                        {integrations.map((item, index) => <div className='integration-box'>
                            <div className='img-wrapper'>
                                <img className='app-icon' src={item.img} />
                            </div>
                            <div className='description'>
                                {item.description}
                            </div>
                            <div className='btn-wrapper'>
                                <button className='integration-button'>
                                    {item.buttonText}
                                </button>
                            </div>
                        </div>)}
                    </div>

                </div>
            </div>
        </>
    </div>
}