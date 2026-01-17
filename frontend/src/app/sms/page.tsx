'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

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
import '@/css/pages/marketing.css'

const smsStats = [
    { mainLabel: 'Total Templates', mainValue: '12', isActive: true },
    { mainLabel: 'Template Types', mainValue: '2', isActive: true },
    { mainLabel: 'SMS Sent', mainValue: '34', isActive: true },
    { mainLabel: 'Active SMS Templates', mainValue: '2', isActive: true },
]

// Form initial Data
const initialAddSmsTemplateData = {
    template_type: '',
    template_name: '',
    active: '',
    agent_send: '',
    marketing: '',
    character_count: '0',
    sms_content: ''
}

const initialUpdateSmsTemplateData = {
    template_type: '',
    template_name: '',
    active: '',
    agent_send: '',
    marketing: '',
    character_count: '0',
    sms_content: ''
}

const fallbackSmsTemplates = [
    { 
        id: 1, 
        template_name: '2FA Verify', 
        template_type: '2FA Verify', 
        character_count: 160, 
        agent_send: true, 
        marketing: true, 
        active: true,
        sms_content: 'The Data Supermarket: 159873 is your code to verify your account. Don\'t share your code.'
    },
    { 
        id: 2, 
        template_name: '2FA Log in', 
        template_type: '2FA Log in', 
        character_count: 160, 
        agent_send: false, 
        marketing: true, 
        active: true,
        sms_content: 'Your login code is 123456. Do not share this code with anyone.'
    },
]

export default function MarketingSmsPage() {
    const { request } = useRequest()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [viewMode, setViewMode] = useState()
    const [smsIndex, setSmsIndex] = useState()
    const [smsDetails, setSmsDetails] = useState()
    const [smsTemplates, setSmsTemplates] = useState(fallbackSmsTemplates)
    const [smsCollection, setSmsCollection] = useState({
        items: fallbackSmsTemplates,
        loaded: false,
        searchParams: new URLSearchParams(),
    })

    // Form handling for add
    const [
        addSmsTemplateData,
        setAddSmsTemplateData,
        onAddSmsTemplateDataInputChange,
        addSmsTemplateDataErrors,
        setAddSmsTemplateDataErrorsMap,
        addSmsTemplateDataErrorMessage,
        setAddSmsTemplateDataErrorMessage,
    ] = useForm(copy(initialAddSmsTemplateData))

    // Form handling for edit
    const [
        updateSmsTemplateData,
        setUpdateSmsTemplateData,
        onUpdateSmsTemplateDataInputChange,
        updateSmsTemplateDataErrors,
        setUpdateSmsTemplateDataErrorsMap,
        updateSmsTemplateDataErrorMessage,
        setUpdateSmsTemplateDataErrorMessage,
    ] = useForm(copy(initialUpdateSmsTemplateData))
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
            name: 'Template Type',
            id: 'template_type',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='template-event'>{row?.template_type}</div>
            ),
        },
        {
            name: 'Character Count',
            id: 'character_count',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='character-count'>{row?.character_count || 0}</div>
            ),
        },
        {
            name: 'Agent Send',
            id: 'agent_send',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span>
                    {row?.agent_send ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: 'Marketing',
            id: 'marketing',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span>
                    {row?.marketing ? 'Yes' : 'No'}
                </span>
            ),
        },
        {
            name: 'Active',
            id: 'active',
            visible: true,
            sortable: 'backend',
            render: row => (
                <span>
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
        async function fetchSmsTemplates() {
            try {
                const [, data] = await request.get('marketing/sms-templates')
                if (Array.isArray(data?.data) && data.data.length) {
                    setSmsTemplates(data.data)
                    updateSmsCollection({ items: data.data, loaded: true })
                    return
                }
            } catch (err) {
                console.warn('Marketing SMS templates API unavailable, using fallback data.')
            }
            updateSmsCollection({ items: fallbackSmsTemplates, loaded: true })
        }

        fetchSmsTemplates()
    }, [request])

    // Fetch detailed template data when a row is clicked (only for view mode)
    useEffect(() => {
        async function fetchTemplateDetails() {
            // Only fetch details in view mode, not in edit mode (edit mode gets data from handleEditClick)
            if (viewMode !== 'view') {
                return
            }
            
            if (smsIndex !== null && smsIndex !== undefined && smsCollection.items[smsIndex]) {
                const templateId = smsCollection.items[smsIndex].id
                try {
                    const [, data] = await request.get(`marketing/sms-templates/${templateId}`)
                    if (data?.data) {
                        setSmsDetails(data.data)
                        return
                    }
                } catch (err) {
                    console.warn('Template details API unavailable, using list data.')
                    // Use the data from the list if detail API fails
                    const template = smsCollection.items[smsIndex]
                    setSmsDetails(template)
                }
            }
        }

        if (smsIndex !== null && smsIndex !== undefined && viewMode === 'view') {
            fetchTemplateDetails()
        }
    }, [smsIndex, request, viewMode])

    const updateSmsCollection = (payload) => {
        setSmsCollection(old => {
            if (payload?.reload) {
                // Reload data from API
                async function reloadData() {
                    try {
                        const [, data] = await request.get('marketing/sms-templates')
                        if (Array.isArray(data?.data) && data.data.length) {
                            setSmsTemplates(data.data)
                            setSmsCollection(prev => ({ ...prev, items: data.data, loaded: true }))
                            return
                        }
                    } catch (err) {
                        console.warn('Marketing SMS templates API unavailable, using fallback data.')
                    }
                    setSmsCollection(prev => ({ ...prev, items: fallbackSmsTemplates, loaded: true }))
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
        const filtered = smsTemplates.filter(template =>
            template.template_name.toLowerCase().includes(query) ||
            template.template_type?.toLowerCase().includes(query)
        )
        updateSmsCollection({ items: filtered })
    }

    // On table row click get the row index and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()
        toggleRightSidePanel()
        setSmsIndex(index)
        setSmsDetails(smsCollection.items[index])
        setViewMode('view')
    }

    // Handle add button click
    const handleAddClick = () => {
        setViewMode('add')
        setAddSmsTemplateData(copy(initialAddSmsTemplateData))
        toggleRightSidePanel()
    }

    // Handle edit button click
    const handleEditClick = (e, index) => {
        e.stopPropagation()
        e.preventDefault()
        const template = smsCollection.items[index]
        
        if (!template) {
            console.warn('Template not found at index:', index)
            return
        }
        
        // Get SMS content and calculate character count
        const smsContent = template?.sms_content || template?.body || ''
        const characterCount = smsContent.length || template?.character_count || 0
        
        // Populate form with template data immediately
        const formData = {
            template_type: template?.template_type || '',
            template_name: template?.template_name || '',
            active: convertBooleanToString(template?.active),
            agent_send: convertBooleanToString(template?.agent_send),
            marketing: convertBooleanToString(template?.marketing),
            character_count: characterCount.toString(),
            sms_content: smsContent
        }
        
        // Set all state at once
        setSmsIndex(index)
        setSmsDetails(template)
        setUpdateSmsTemplateData(formData)
        setViewMode('edit')
        toggleRightSidePanel()
    }

    // Helper function to convert 'yes'/'no' strings to boolean
    const convertStringToBoolean = (value) => {
        if (value === 'yes' || value === 'Yes' || value === true) return true
        if (value === 'no' || value === 'No' || value === false) return false
        return false
    }

    // Handle save (add or update)
    const handleSave = async (e) => {
        e.preventDefault()
        const formData = viewMode === 'add' ? addSmsTemplateData : updateSmsTemplateData
        
        // Transform data to match backend expectations
        const data = {
            template_type: formData.template_type || null,
            template_name: formData.template_name || '',
            active: convertStringToBoolean(formData.active),
            agent_send: convertStringToBoolean(formData.agent_send),
            marketing: convertStringToBoolean(formData.marketing),
            character_count: formData.character_count ? parseInt(formData.character_count, 10) : 0,
            sms_content: formData.sms_content || formData.body || '',
            body: formData.sms_content || formData.body || '', // Some APIs might expect 'body' instead of 'sms_content'
        }
        
        try {
            if (viewMode === 'add') {
                await request.post('marketing/sms-templates', data)
                setAddSmsTemplateData(copy(initialAddSmsTemplateData))
            } else {
                const templateId = smsCollection.items[smsIndex]?.id
                await request.patch(`marketing/sms-templates/${templateId}`, data)
            }
            updateSmsCollection({ reload: true })
            toggleRightSidePanel()
        } catch (err) {
            console.error('Failed to save template:', err)
        }
    }

    // Store key value pair to pass into KeyValue Component for SMS template details
    const smsTemplateKeyValueDataList = [
        {
            property: 'template_type',
            value: smsDetails?.template_type || 'N/A',
            displayKey: 'Template Type'
        },
        {
            property: 'template_name',
            value: smsDetails?.template_name || 'N/A',
            displayKey: 'Template Name'
        },
        {
            property: 'active',
            value: smsDetails?.active ? 'Yes' : 'No',
            displayKey: 'Active'
        },
        {
            property: 'agent_send',
            value: smsDetails?.agent_send ? 'Yes' : 'No',
            displayKey: 'Agent Send'
        },
        {
            property: 'marketing',
            value: smsDetails?.marketing ? 'Yes' : 'No',
            displayKey: 'Marketing'
        },
        {
            property: 'character_count',
            value: smsDetails?.character_count?.toString() || '0',
            displayKey: 'Character Count'
        },
        {
            property: 'sms_content',
            value: smsDetails?.sms_content || smsDetails?.body || 'N/A',
            displayKey: 'SMS Content',
            name: 'long-text'
        },
    ]

    const subNavItems = [
        { label: 'Templates', href: '/marketing' },
        { label: 'Email', href: '/marketing/email' },
        { label: 'SMS', href: '/marketing/sms', active: true },
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
                        statValues={smsStats}
                        isDateDropList={false}
                        isDateInput={true}
                    />
                    <div className='table-wrapper'>
                        <div className='table-container'>
                            <TablePageHeader
                                title='SMS Templates'
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
                                items={smsCollection.items}
                                onRowClick={onRowClick}
                                columns={columns}
                                controlColumns={[]}
                                loaded={smsCollection.loaded}
                                searchParams={smsCollection.searchParams}
                                collection={smsCollection}
                                updateCollection={updateSmsCollection}
                                selectedIndex={smsIndex}
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
                        setSmsIndex(null)
                    }}
                >
                    <RightSidePanel
                        key={`sms-${viewMode}-${smsIndex}`}
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
                        details={smsDetails}
                        setDetails={setSmsDetails}
                        buttonOneFunction={
                            viewMode === 'view'
                                ? () => {
                                    const newIndex = smsIndex - 1
                                    if (newIndex >= 0) {
                                        setSmsIndex(newIndex)
                                        setSmsDetails(smsCollection.items[newIndex])
                                    }
                                }
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? toggleRightSidePanel
                                    : null
                        }
                        buttonTwoFunction={
                            viewMode === 'view'
                                ? () => {
                                    const newIndex = smsIndex + 1
                                    if (newIndex < smsCollection.items.length) {
                                        setSmsIndex(newIndex)
                                        setSmsDetails(smsCollection.items[newIndex])
                                    }
                                }
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? handleSave
                                    : null
                        }
                        updateData={
                            viewMode === 'edit'
                                ? updateSmsTemplateData
                                : viewMode === 'add'
                                    ? addSmsTemplateData
                                    : null
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateSmsTemplateDataInputChange
                                : viewMode === 'add'
                                    ? onAddSmsTemplateDataInputChange
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
                        setIndex={setSmsIndex}
                        index={smsIndex}
                        collection={smsCollection}
                        page='sms-template'
                        keyValueDataList={smsTemplateKeyValueDataList}
                    />
                </div>
            )}
        </div>
    )
}

