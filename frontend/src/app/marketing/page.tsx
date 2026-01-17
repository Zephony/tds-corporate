'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Stats from '@/components/stats'
import Table from '@/components/table'
import TablePageHeader from '@/components/tablePageHeader'

import useRequest from '@/hooks/useRequest'
import useToggle from '@/hooks/useToggle'
import '@/css/pages/marketing.css'

const marketingStats = [
    { mainLabel: 'Total Templates', mainValue: '12', isActive: true },
    { mainLabel: 'Email Template', mainValue: '8', isActive: true },
    { mainLabel: 'SMS Template', mainValue: '4', isActive: true },
    { mainLabel: 'Templates Added', mainValue: '2', isActive: true },
]

const fallbackTemplates = [
    { id: 1, template_name: 'Forgot Password Email', event: 'Forget Password', channel: 'Email' },
    { id: 2, template_name: 'Welcome Email (Sign Up)', event: 'New User Registration', channel: 'Email' },
    { id: 3, template_name: 'Account Verification Email', event: 'Verify Account', channel: 'Email' },
    { id: 4, template_name: 'Order Confirmation Email (for leads)', event: 'Order Confirmation (Leads)', channel: 'Email' },
    { id: 5, template_name: 'Purchase Confirmation Email (for data)', event: 'Order Confirmation (Data)', channel: 'Email' },
    { id: 6, template_name: 'Lead Delivery Email', event: 'Lead Delivery', channel: 'Email' },
]

export default function MarketingTemplatesPage() {
    const { request } = useRequest()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [viewMode, setViewMode] = useState<'view' | 'add'>('view')
    const [templatesData, setTemplatesData] = useState(fallbackTemplates)
    const [templatesCollection, setTemplatesCollection] = useState({
        items: fallbackTemplates,
        loaded: false,
        searchParams: new URLSearchParams(),
    })
    const [columns] = useState([
        {
            name: 'Template Name',
            id: 'template_name',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='template-meta'>
                    <div className='template-name'>{row?.template_name}</div>
                </div>
            ),
        },
        {
            name: 'Event',
            id: 'event',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='template-event'>{row?.event}</div>
            ),
        },
        {
            name: 'Channel',
            id: 'channel',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span className={`channel-chip ${row?.channel?.toLowerCase() === 'sms' ? 'sms' : ''}`}>
                    {row?.channel || 'Email'}
                </span>
            ),
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            render: () => (
                <button className='delete-icon-wrapper' title='Delete Template'>
                    <img className='delete-icon' src='/delete-icon.svg' alt='Delete' />
                </button>
            ),
        },
    ])

    useEffect(() => {
        async function fetchTemplates() {
            try {
                const [, data] = await request.get('marketing/templates')
                if (Array.isArray(data?.data) && data.data.length) {
                    setTemplatesData(data.data)
                    updateTemplatesCollection({ items: data.data, loaded: true })
                    return
                }
            } catch (err) {
                console.warn('Marketing templates API unavailable, using fallback data.')
            }
            updateTemplatesCollection({ items: fallbackTemplates, loaded: true })
        }

        fetchTemplates()
    }, [request])

    const updateTemplatesCollection = (payload) => {
        setTemplatesCollection(old => {
            const updates = typeof payload === 'function' ? payload(old) : payload
            return { ...old, ...updates }
        })
    }

    const handleSearch = (value: string, updateCollectionCb = updateTemplatesCollection) => {
        const query = value.toLowerCase()
        const filtered = templatesData.filter(template =>
            template.template_name.toLowerCase().includes(query) ||
            template.event.toLowerCase().includes(query)
        )
        updateCollectionCb({ items: filtered })
    }

    const subNavItems = [
        { label: 'Templates', href: '/marketing', active: true },
        { label: 'Email', href: '/marketing/email' },
        { label: 'SMS', href: '/marketing/sms' },
    ]

    return (
        <div className='page-container marketing-page'>
            <div className='left-container'>
                <Menubar />
            </div>
            <div className='main-content'>
                <Header title='Marketing' />
                <div className='main-content-body'>
                    <Stats
                        statValues={marketingStats}
                        isDateDropList={false}
                        isDateInput={true}
                    />
                    <div className='marketing-table-wrapper'>
                        <div className='marketing-sub-nav'>
                            {subNavItems.map(tab => (
                                <Link
                                    key={tab.label}
                                    href={tab.disabled ? '#' : tab.href}
                                    className={`marketing-sub-nav-item ${tab.active ? 'active' : ''} ${tab.disabled ? 'disabled' : ''}`}
                                    aria-disabled={tab.disabled}
                                >
                                    {tab.label}
                                </Link>
                            ))}
                        </div>
                        <div className='marketing-table-header'>
                            <TablePageHeader
                                title='Templates'
                                onSearch={handleSearch}
                                updateCollection={updateTemplatesCollection}
                                showActionButtons
                                onAddClick
                                buttonText='Assign Template'
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <div className='marketing-extra-actions'>
                                <button 
                                    className='marketing-action-btn primary'
                                    onClick={() => {
                                        // Handle Send Email action
                                        console.log('Send Email clicked')
                                    }}
                                >
                                    Send Email
                                </button>
                            </div>
                        </div>
                        <Table
                            className='category-table'
                            items={templatesCollection.items}
                            columns={columns}
                            controlColumns={[]}
                            loaded={templatesCollection.loaded}
                            searchParams={templatesCollection.searchParams}
                            collection={templatesCollection}
                            updateCollection={updateTemplatesCollection}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

