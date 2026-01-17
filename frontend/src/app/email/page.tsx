'use client'

import { useState, useEffect } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Stats from '@/components/stats'
import Table from '@/components/table'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'

import useRequest from '@/hooks/useRequest'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'
import { copy } from '@/helpers'

const emailStats = [
    { mainLabel: 'Total Templates', mainValue: '12', isActive: true },
    { mainLabel: 'Event Types', mainValue: '8', isActive: true },
    { mainLabel: 'Emails Sent', mainValue: '154', isActive: true },
    { mainLabel: 'Active Email Templates', mainValue: '11', isActive: true },
]

// Form initial Data
const initialAddEmailTemplateData = {
    template_name: '',
    active: '',
    agent_active: '',
    attachment: '',
    client_view: '',
    to: '',
    cc: '',
    bcc: '',
    subject: '',
    message: ''
}

const initialUpdateEmailTemplateData = {
    template_name: '',
    active: '',
    agent_active: '',
    attachment: '',
    client_view: '',
    to: '',
    cc: '',
    bcc: '',
    subject: '',
    message: ''
}

const fallbackEmailTemplates = [
    { 
        id: 1, 
        template_name: 'Welcome Email (Sign Up)', 
        attachment: true, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Welcome to The Data Supermarket - Your Shopping Journey Begins!',
        message: 'Dear $first_name,\n\nWelcome to The Data Supermarket! We\'re thrilled to have you join our community of shoppers. Get ready to explore an exciting world of Data & Live Leads with unparalleled payment protection, all at your fingertips.\n\nHere\'s what you can do:\n1-Browse, compare & purchase online..\n2-Discover unique items from our amazing sellers.\n3-Enjoy secure transactions for a worry-free shopping experience.\n\nNeed assistance? Don\'t hesitate to contact our support team at help@thedatasupermarket.com or visit our Help Centre $help_centre_link.\n\nStart exploring and happy shopping!\n\nBest regards,\nThe Data Supermarket Team'
    },
    { 
        id: 2, 
        template_name: 'Account Verification Email', 
        attachment: false, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Verify Your Account',
        message: 'Please verify your account by clicking the link below.'
    },
    { 
        id: 3, 
        template_name: 'Order Confirmation Email (for leads)', 
        attachment: false, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Order Confirmation',
        message: 'Your order has been confirmed.'
    },
    { 
        id: 4, 
        template_name: 'Purchase Confirmation Email (for data)', 
        attachment: true, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Purchase Confirmation',
        message: 'Your purchase has been confirmed.'
    },
    { 
        id: 5, 
        template_name: 'Lead Delivery Email', 
        attachment: true, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Lead Delivery',
        message: 'Your leads have been delivered.'
    },
    { 
        id: 6, 
        template_name: 'Review Your Purchase', 
        attachment: true, 
        agent_active: true, 
        client_view: true, 
        active: true,
        to: '$email',
        cc: 'NA',
        bcc: 'NA',
        subject: 'Review Your Purchase',
        message: 'Please review your recent purchase.'
    },
]

export default function MarketingEmailPage() {
    const { request } = useRequest()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [viewMode, setViewMode] = useState()
    const [emailIndex, setEmailIndex] = useState()
    const [emailDetails, setEmailDetails] = useState()
    const [emailTemplates, setEmailTemplates] = useState(fallbackEmailTemplates)
    const [emailCollection, setEmailCollection] = useState({
        items: fallbackEmailTemplates,
        loaded: false,
        searchParams: new URLSearchParams(),
    })

    // Form handling for add
    const [
        addEmailTemplateData,
        setAddEmailTemplateData,
        onAddEmailTemplateDataInputChange,
        addEmailTemplateDataErrors,
        setAddEmailTemplateDataErrorsMap,
        addEmailTemplateDataErrorMessage,
        setAddEmailTemplateDataErrorMessage,
    ] = useForm(copy(initialAddEmailTemplateData))

    // Form handling for edit
    const [
        updateEmailTemplateData,
        setUpdateEmailTemplateData,
        onUpdateEmailTemplateDataInputChange,
        updateEmailTemplateDataErrors,
        setUpdateEmailTemplateDataErrorsMap,
        updateEmailTemplateDataErrorMessage,
        setUpdateEmailTemplateDataErrorMessage,
    ] = useForm(copy(initialUpdateEmailTemplateData))
    const [columns] = useState([
        {
            name: 'Template Name',
            id: 'template_name',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='template-name'>{row?.template_name}</div>
            ),
        },
        {
            name: 'Attachment',
            id: 'attachment',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span className={`status-pill ${row?.attachment ? 'yes' : 'no'}`}>
                    {row?.attachment ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: 'Agent Active',
            id: 'agent_active',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span className={`status-pill ${row?.agent_active ? 'yes' : 'no'}`}>
                    {row?.agent_active ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: 'Client View',
            id: 'client_view',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span className={`status-pill ${row?.client_view ? 'yes' : 'no'}`}>
                    {row?.client_view ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: 'Active',
            id: 'active',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span className={`status-pill ${row?.active ? 'yes' : 'no'}`}>
                    {row?.active ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: '',
            id: 'action',
            visible: true,
            render: (row, customData, collection, updateCollection, index) => (
                <div className='action'>
                    <button 
                        className='edit-icon-wrapper' 
                        title='Edit Template'
                        onClick={(e) => handleEditClick(e, index)}
                    >
                        <img className='edit-icon' src='/edit-icon.svg' alt='Edit' />
                    </button>
                    <button className='delete-icon-wrapper' title='Delete Template'>
                        <img className='delete-icon' src='/delete-icon.svg' alt='Delete' />
                    </button>
                </div>
            ),
        },
    ])

    

    useEffect(() => {
        async function fetchEmailTemplates() {
            try {
                const [, data] = await request.get('marketing/email-templates')
                if (Array.isArray(data?.data) && data.data.length) {
                    setEmailTemplates(data.data)
                    updateEmailCollection({ items: data.data, loaded: true })
                    return
                }
            } catch (err) {
                console.warn('Marketing email templates API unavailable, using fallback data.')
            }
            updateEmailCollection({ items: fallbackEmailTemplates, loaded: true })
        }

        fetchEmailTemplates()
    }, [request])

    // Fetch detailed template data when a row is clicked
    useEffect(() => {
        async function fetchTemplateDetails() {
            if (emailIndex !== null && emailIndex !== undefined && emailCollection.items[emailIndex]) {
                const templateId = emailCollection.items[emailIndex].id
                try {
                    const [, data] = await request.get(`marketing/email-templates/${templateId}`)
                    if (data?.data) {
                        setEmailDetails(data.data)
                        // If in edit mode, update form data
                        if (viewMode === 'edit') {
                            setUpdateEmailTemplateData({
                                template_name: data.data?.template_name || '',
                                active: convertBooleanToString(data.data?.active),
                                agent_active: convertBooleanToString(data.data?.agent_active),
                                attachment: convertBooleanToString(data.data?.attachment),
                                client_view: convertBooleanToString(data.data?.client_view),
                                to: data.data?.to || '',
                                cc: data.data?.cc || '',
                                bcc: data.data?.bcc || '',
                                subject: data.data?.subject || '',
                                message: data.data?.message || data.data?.body || ''
                            })
                        }
                        return
                    }
                } catch (err) {
                    console.warn('Template details API unavailable, using list data.')
                    // Use the data from the list if detail API fails
                    const template = emailCollection.items[emailIndex]
                    setEmailDetails(template)
                    // If in edit mode, update form data
                    if (viewMode === 'edit') {
                        setUpdateEmailTemplateData({
                            template_name: template?.template_name || '',
                            active: convertBooleanToString(template?.active),
                            agent_active: convertBooleanToString(template?.agent_active),
                            attachment: convertBooleanToString(template?.attachment),
                            client_view: convertBooleanToString(template?.client_view),
                            to: template?.to || '',
                            cc: template?.cc || '',
                            bcc: template?.bcc || '',
                            subject: template?.subject || '',
                            message: template?.message || template?.body || ''
                        })
                    }
                }
            }
        }

        if (emailIndex !== null && emailIndex !== undefined) {
            fetchTemplateDetails()
        }
    }, [emailIndex, request, viewMode])

    const updateEmailCollection = (payload) => {
        setEmailCollection(old => {
            if (payload?.reload) {
                // Reload data from API
                async function reloadData() {
                    try {
                        const [, data] = await request.get('marketing/email-templates')
                        if (Array.isArray(data?.data) && data.data.length) {
                            setEmailTemplates(data.data)
                            setEmailCollection(prev => ({ ...prev, items: data.data, loaded: true }))
                            return
                        }
                    } catch (err) {
                        console.warn('Marketing email templates API unavailable, using fallback data.')
                    }
                    setEmailCollection(prev => ({ ...prev, items: fallbackEmailTemplates, loaded: true }))
                }
                reloadData()
                return old
            }
            const updates = typeof payload === 'function' ? payload(old) : payload
            return { ...old, ...updates }
        })
    }

    // Helper function to convert boolean/string values to 'yes'/'no' for dropdowns
    const convertBooleanToString = (value) => {
        if (value === true || value === 'true' || value === 'yes' || value === 'Yes') return 'yes'
        if (value === false || value === 'false' || value === 'no' || value === 'No') return 'no'
        return value || ''
    }

    const handleSearch = (value: string) => {
        const query = value.toLowerCase()
        const filtered = emailTemplates.filter(template =>
            template.template_name.toLowerCase().includes(query)
        )
        updateEmailCollection({ items: filtered })
    }

    // On table row click get the row index and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()
        toggleRightSidePanel()
        setEmailIndex(index)
        setEmailDetails(emailCollection.items[index])
        setViewMode('view')
    }

    // Handle add button click
    const handleAddClick = () => {
        setViewMode('add')
        setAddEmailTemplateData(copy(initialAddEmailTemplateData))
        toggleRightSidePanel()
    }

    // Handle edit button click
    const handleEditClick = (e, index) => {
        e.stopPropagation()
        const template = emailCollection.items[index]
        
        if (!template) {
            console.warn('Template not found at index:', index)
            return
        }
        
        // Populate form with template data
        const formData = {
            template_name: template?.template_name || '',
            active: convertBooleanToString(template?.active),
            agent_active: convertBooleanToString(template?.agent_active),
            attachment: convertBooleanToString(template?.attachment),
            client_view: convertBooleanToString(template?.client_view),
            to: template?.to || '',
            cc: template?.cc || '',
            bcc: template?.bcc || '',
            subject: template?.subject || '',
            message: template?.message || template?.body || ''
        }
        
        setViewMode('edit')
        setEmailIndex(index)
        setUpdateEmailTemplateData(formData)
        setEmailDetails(template)
        toggleRightSidePanel()
    }

    // Handle save (add or update)
    const handleSave = async (e) => {
        e.preventDefault()
        const data = viewMode === 'add' ? addEmailTemplateData : updateEmailTemplateData
        
        try {
            if (viewMode === 'add') {
                await request.post('marketing/email-templates', data)
                setAddEmailTemplateData(copy(initialAddEmailTemplateData))
            } else {
                const templateId = emailCollection.items[emailIndex]?.id
                await request.patch(`marketing/email-templates/${templateId}`, data)
            }
            updateEmailCollection({ reload: true })
            toggleRightSidePanel()
        } catch (err) {
            console.error('Failed to save template:', err)
        }
    }

    // Store key value pair to pass into KeyValue Component for email template details
    const emailTemplateKeyValueDataList = [
        {
            property: 'template_name',
            value: emailDetails?.template_name || 'N/A',
            displayKey: 'Template Name'
        },
        {
            property: 'to',
            value: emailDetails?.to || '$email',
            displayKey: 'To'
        },
        {
            property: 'cc',
            value: emailDetails?.cc || 'NA',
            displayKey: 'CC'
        },
        {
            property: 'bcc',
            value: emailDetails?.bcc || 'NA',
            displayKey: 'BCC'
        },
        {
            property: 'subject',
            value: emailDetails?.subject || 'N/A',
            displayKey: 'Subject'
        },
        {
            property: 'message',
            value: emailDetails?.message || emailDetails?.body || 'N/A',
            displayKey: 'Message',
            name: 'long-text'
        },
    ]

    const subNavItems = [
        { label: 'Templates', href: '/marketing' },
        { label: 'Email', href: '/marketing/email', active: true },
        { label: 'SMS', href: '#', disabled: true },
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
                        statValues={emailStats}
                        isDateDropList={false}
                        isDateInput={true}
                    />
                    <div className='table-wrapper'>
                        <div className='table-container'>
                            <TablePageHeader
                                title='Email Templates'
                                onSearch={handleSearch}
                                onAddClick={handleAddClick}
                                onExportClick={null}
                                showActionButtons
                                buttonText='Add Template'
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <Table
                                className='category-table'
                                items={emailCollection.items}
                                onRowClick={onRowClick}
                                columns={columns}
                                controlColumns={[]}
                                loaded={emailCollection.loaded}
                                searchParams={emailCollection.searchParams}
                                collection={emailCollection}
                                updateCollection={updateEmailCollection}
                                selectedIndex={emailIndex}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Right Side Panel */}
            {showRightSidePanel && (
                <div
                    className='overlay'
                    onClick={() => {
                        toggleRightSidePanel()
                        setEmailIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Template Details'
                                : viewMode === 'edit'
                                    ? 'Edit Template'
                                    : viewMode === 'add'
                                        ? 'Add Template'
                                        : ''
                        }
                        details={emailDetails}
                        setDetails={setEmailDetails}
                        buttonOneFunction={
                            viewMode === 'view'
                                ? () => {
                                    const newIndex = emailIndex - 1
                                    if (newIndex >= 0) {
                                        setEmailIndex(newIndex)
                                        setEmailDetails(emailCollection.items[newIndex])
                                    }
                                }
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? toggleRightSidePanel
                                    : null
                        }
                        buttonTwoFunction={
                            viewMode === 'view'
                                ? () => {
                                    const newIndex = emailIndex + 1
                                    if (newIndex < emailCollection.items.length) {
                                        setEmailIndex(newIndex)
                                        setEmailDetails(emailCollection.items[newIndex])
                                    }
                                }
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? handleSave
                                    : null
                        }
                        updateData={
                            viewMode === 'edit'
                                ? updateEmailTemplateData
                                : viewMode === 'add'
                                    ? addEmailTemplateData
                                    : null
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateEmailTemplateDataInputChange
                                : viewMode === 'add'
                                    ? onAddEmailTemplateDataInputChange
                                    : null
                        }
                        buttonNameOne='without-bg-btn'
                        buttonNameTwo='with-bg-btn'
                        buttonTextOne={
                            viewMode === 'view'
                                ? 'Previous Template'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next Template'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setEmailIndex}
                        index={emailIndex}
                        collection={emailCollection}
                        page='email-template'
                        keyValueDataList={emailTemplateKeyValueDataList}
                    />
                </div>
            )}
        </div>
    )
}

