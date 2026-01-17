'use client'

import { useState, useRef, useEffect } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import Stats from '@/components/stats'
import RightSidePanel from '@/components/rightSidePanel'
import Modal from '@/components/modal'
import Link from 'next/link'

import { formatDateTime, shortenText } from '@/helpers'
import { copy } from '@/helpers'
import { replaceUnderScoreWithSpace } from '@/helpers'

import useRequest from '@/hooks/useRequest'
import useFilter from '@/hooks/useFilter'
import useToggle from '@/hooks/useToggle'
import useQueryParams from '@/hooks/useQueryParams'
import useCollection from '@/hooks/useCollection'
import { useForm } from '@/hooks/useForm'
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

import '@/css/pages/product.css'
const stats = [
    {
        mainLabel: 'Total Listing',
        mainValue: '765',
        subLabel: 'Waiting for approval',
        subValue: '12',
        isActive: true
    },
    {
        mainLabel: 'Active Listing',
        mainValue: '685',
        subLabel: 'Rejected / Expired',
        subValue: '36 / 27',
        isActive: true

    },
    {
        mainLabel: 'Dataset',
        mainValue: '510',
        subLabel: 'Pending Dataset',
        subValue: '7',
        isActive: true

    },
    {
        mainLabel: 'Live Leads',
        mainValue: '255',
        subLabel: 'Pending Live Leads',
        subValue: '4',
        isActive: true
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
]

const quickFilter = [
    {
        label: 'Show Dataset',
        key: 'show_dataset',
        isActive: true
    },
    {
        label: 'Show Live Leads',
        key: 'show_live_leads',
        isActive: false
    },
    {
        label: 'Show Pending',
        key: 'show_pending',
        isActive: false
    },
    {
        label: 'Show Rejected',
        key: 'show_rejected',
        isActive: true
    },
]

const initialFilterData = {
    f_user_status: {
        operator: 'equals',
        value: '',
        type: 'checkbox'
    }
}

// Form initial Data
const initialUpdateProductData = {
    name: '',
    email: '',
    phone: '',
    company_name: '',
    company_registration_no: '',
    address: '',
    city: '',
    pincode: '',
    company_website: '',
    business_category: '',
    business_sub_category: '',
    company_phone: '',
    company_postion: '',
    icno_no: '',
    status: '',
    country: '',
    place: ''
}

// Form initial Data
const initialAddProductData = {
    first_name: '',
    last_name: '',
    email: '',
    user_status: '',
    id_company: '',
    status: '',
    total_purchases: '',
    total_disputes: '',
    first_purchase_date: '',
    last_purchase_date: '',
    notes: ''
}

export default function Product() {
    const { request } = useRequest()

    // Used to toggle RightSidePanle, FilterDropList , TeamDetailsModal, DeleteModal
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showTeamModal, toggleTeamModal] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()
    const [showKeywordsModal, toggleKeywordsModal] = useToggle()
    const [type, setType] = useState()
    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'Signed up on',
            id: 'signed_up_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='signed-up'>
                {formatDateTime(row?.created_at)}
            </div>
        },
        {
            name: 'Company Name',
            id: 'company_details_.name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='company-details-product'>
                <div className='company-place'>
                    <img className='country-icon' src='/country.svg' />
                </div>
                <div
                    title={row?.name}
                    className='company-name'
                >
                    {shortenText(row?.name)}
                </div>
            </div>
        },
        {
            name: 'Product',
            id: 'name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='user-name'>
                <div className='link-like-button'>
                    {row?.name}
                </div>
            </div>
        },
        {
            name: 'Type',
            id: 'total_purchases',
            visible: true,
            sortable: 'backend',
            render: row => <div className='purchases'>
                {row?.product_type === 'LIVE_LEADS' ? 'Live Leads' : 'Dataset'}
            </div>
        },
        {
            name: 'Options Added',
            id: 'total_disputes',
            visible: true,
            sortable: 'backend',
            render: row => <div className='disputed'>
                <div className='options-added' title={row?.geographic_coverage}>
                    {(() => {
                        const word = row?.geographic_coverage?.split(' ') || []
                        const first = word[0]?.[0] || ''
                        const second = word[1]?.[0] || ''
                        return `${first}${second}`
                    })()}
                </div>
            </div>
        },
        {
            name: 'Source Passed',
            id: 'source_passed',
            visible: true,
            sortable: 'backend',
            render: row => <div className='disputed'>
                <div className='disputes'>
                    {row?.data_source_name ? 'Yes ' : 'No'}
                    
                    {row?.data_source_name 
                        ? <Link href={row?.source_url} target='_blank' className='link-like-button' onClick={(e) => e.stopPropagation()}>
                            View Source
                        </Link> 
                        : ''
                    }
                </div>
            </div>
        },
        {
            name: 'Status',
            id: 'approval_status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                title={replaceUnderScoreWithSpace(row?.status)}
                className={`status-main ${row?.status === 'APPROVED'
                        ? 'green'
                        : row?.status === 'PENDING_APPROVAL'
                            ? 'yellow'
                            : 'grey'
                    }`}
            >
                {shortenText(replaceUnderScoreWithSpace(row?.status))}
            </div>
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => <div className='action'>
                <div className='action-button'>
                    <button
                        onClick={(e) => {
                            e.stopPropagation()
                            setViewMode('edit')
                            toggleRightSidePanel()
                            setClickedProductIndex(index)
                            setActiveTab('basic_details')
                            setUpdateProductData({
                                first_name: row.name,
                                last_name: row.name,
                                email: row.email,
                                phone: row?.company_details?.phone,
                                company_name: row?.company_details?.name,
                                total_disputes: row.total_disputes,
                                status: row?.status,
                                company_registration_no: row?.company_details?.registration_number,
                                address: '123 Rosewood Lane Bristol BS1 4XY United Kingdom',
                                place: 'Cambridge',
                                pincode: 'EC4N 6AF',
                                company_website: 'https://www.testcompany.co.uk',
                                business_category: 'Retail & E-commerce',
                                business_sub_category: 'Online Marketplace',
                                company_phone: row?.company_details?.phone,
                                company_position: 'CEO (Chief Executive Officer)',
                                icno_no: row?.company_details?.ico_number,
                                city: 'Cambridge',
                                country: 'United Kingdom',
                            })
                        }}
                        className='edit-icon-wrapper'
                    >
                        <img
                            className='edit-icon'
                            src='/edit-icon.svg'
                        />
                    </button>
                    <button
                        className='delete-icon-wrapper'
                        onClick={(e) => {
                            e.stopPropagation()
                            setDeleteModalDescription('Are you sure, want to delete this product')
                            setDeleteModalTitle('Delete Product')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setBuyerByCompanyId(row.id)
                        }}
                    >
                        <img
                            className='delete-icon'
                            src='/delete-icon.svg'
                        />
                    </button>
                </div>
            </div>
        },
    ])

    // Set query params
    const [queryParams, setQueryParam, updateQueryParam] = useQueryParams()

    // Stores Buyers data
    const [productC, updateProductC] = useCollection('admin/products', null, null)

    // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData
    ] = useFilter(initialFilterData, updateProductC)

    const [
        addProductData,
        setAddProductData,
        onAddProductDataInputChange,
        addProductDataErrors,
        setAddProductDataErrorsMap,
        addProductDataErrorMessage,
        setAddProductDataErrorMessage,
    ] = useForm(copy(initialAddProductData))

    // Create the form for editng the buyer Data
    const [
        updateProductData,
        setUpdateProductData,
        onUpdateProductDataInputChange,
        updateProductDataErrors,
        setUpdateProductDataErrorsMap,
        updateProductDataErrorMessage,
        setUpdateProductDataErrorMessage,
    ] = useForm(copy(initialUpdateProductData))

    // Store the clicked buyer from table row click
    const [productDetails, setProductDetails] = useState()


    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    // Clicked Buyer Index
    const [clickedProductIndex, setClickedProductIndex] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [productIndex, setProductIndex] = useState()

    // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view': {
            'basic_details': {
                label: 'Basic Details'
            },
            'paper_trail': {
                label: 'Paper Trail'
            },
            'source': {
                label: 'Source'
            },
            'qty_pricing': {
                label: 'Qty Pricing'
            },
        },
        'edit': {
            // No tabs for edit mode
        }
    })

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    // Sets the active tab when user clicks on 
    // it by defail 'basic_details' will be the tab selected
    const [activeTab, setActiveTab] = useState('basic_details')

    const [message, setMessage] = useState([])

    // Helper function to format date
    const formatDate = (dateString) => {
        if (!dateString) return '--'
        const date = new Date(dateString)
        if (Number.isNaN(date.getTime())) return '--'
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        })
    }

    // Helper function to calculate valid upto date
    const calculateValidUpto = (months, startDate = null) => {
        if (!months) return 'Nil'
        const baseDate = startDate ? new Date(startDate) : new Date()
        const resultDate = new Date(baseDate)
        resultDate.setMonth(resultDate.getMonth() + months)
        return formatDate(resultDate.toISOString())
    }

    // Store key value pair to pass into KeyValue Component
    const keyValueDataList = [
        // Basic Product Information Section
        {
            property: 'category',
            value: productDetails?.category_name || productDetails?.category_details?.name || '--',
            displayKey: 'Category',
            subValue: null
        },
        {
            property: 'total_records',
            value: productDetails?.total_records?.toLocaleString() || productDetails?.uploaded_records?.toLocaleString() || '0',
            displayKey: 'Uploaded Records',
            subValue: null
        },
        {
            property: 'accepted_records',
            value: productDetails?.accepted_records?.toLocaleString() || productDetails?.available_records?.toLocaleString() || '0',
            displayKey: 'Accepted Records',
            subValue: null
        },
        {
            property: 'tps_matched',
            value: productDetails?.tps_matched_records?.toLocaleString() || '0',
            displayKey: 'Records matched with TPS',
            subValue: null
        },
        {
            property: 'full_file_price',
            value: productDetails?.price ? `£${parseFloat(productDetails.price).toFixed(2)}` : '--',
            displayKey: 'Full File Price',
            subValue: null
        },
        {
            property: 'cost_per_row',
            value: productDetails?.cost_per_row ? `£${parseFloat(productDetails.cost_per_row).toFixed(2)}` : 
                   (productDetails?.price && productDetails?.total_records ? 
                    `£${(parseFloat(productDetails.price) / productDetails.total_records).toFixed(2)}` : '--'),
            displayKey: 'Cost Per Row',
            subValue: null
        },
        {
            property: 'data_type',
            value: replaceUnderScoreWithSpace(productDetails?.data_type) || '--',
            displayKey: 'Data Type',
            subValue: null
        },
        {
            property: 'sale_type',
            value: replaceUnderScoreWithSpace(productDetails?.sale_type) || '--',
            displayKey: 'Sale Type',
            subValue: null
        },
        {
            property: 'contact_methods',
            value: productDetails?.contact_methods || '--',
            displayKey: 'Contact Method',
            subValue: null
        },
        {
            property: 'replacement_policy',
            value: replaceUnderScoreWithSpace(productDetails?.replacement_policy) || 'N/A',
            displayKey: 'Replacement',
            subValue: null
        },
        {
            property: 'source_url',
            value: productDetails?.source_url ? <Link href={productDetails?.source_url} target='_blank' className='link-like-button' onClick={(e) => e.stopPropagation()}>
                {productDetails?.source_url}
            </Link> : '--',
            displayKey: 'Source URL',
            subValue: null
        },
    ]

    const keyValueDataListTwo = [
        // Divider line will be added automatically after these items
        // Product Duration & Usage Limit Section
        {
            property: 'listing_period',
            value: productDetails?.listing_period_months ? `${productDetails.listing_period_months} months` : '--',
            displayKey: 'Listing Period',
            subValue: productDetails?.listing_period_months ? 
                     `Valid upto: ${calculateValidUpto(productDetails.listing_period_months, productDetails?.created_at)}` : null
        },
        {
            property: 'license_period',
            value: productDetails?.license_period_months ? `${productDetails.license_period_months} months` : '--',
            displayKey: 'License Period',
            subValue: productDetails?.license_period_months ? 
                     `Valid upto: ${calculateValidUpto(productDetails.license_period_months, productDetails?.created_at)}` : null
        },
        {
            property: 'usage_limit',
            value: replaceUnderScoreWithSpace(productDetails?.usage_limit_type) || 'Unlimited',
            displayKey: 'Usage Limit',
            subValue: productDetails?.usage_limit_type === 'UNLIMITED' ? 'Valid upto: Nil' : 
                     (productDetails?.usage_limit_expiry ? `Valid upto: ${formatDate(productDetails.usage_limit_expiry)}` : null)
        },
        {
            property: 'geographic_coverage',
            value: productDetails?.geographic_coverage || '--',
            displayKey: 'Geo Coverage',
            subValue: null
        },
        {
            property: 'restricted_use',
            value: productDetails?.restricted_use || '--',
            displayKey: 'Restricted Use',
            subValue: null
        },
    ]

    const keyValueDataListThree = [
        // Data Validations Section
        {
            property: 'paf_cleanse',
            value: formatDate(productDetails?.paf_cleanse_date) || '--',
            displayKey: 'PAF Cleanse',
            subValue: null
        },
        {
            property: 'email_validations',
            value: formatDate(productDetails?.email_validation_date) || '--',
            displayKey: 'Email Validations',
            subValue: null
        },
        {
            property: 'movers_deceased',
            value: formatDate(productDetails?.movers_deceased_cleanse_date) || '--',
            displayKey: 'Movers/Deceased Cleanse',
            subValue: null
        },
        {
            property: 'hlr_llv',
            value: formatDate(productDetails?.hlr_check_date) || formatDate(productDetails?.llv_check_date) || '--',
            displayKey: 'HLR/LLV',
            subValue: null
        },
        {
            property: 'tps_check',
            value: formatDate(productDetails?.tps_check_date) || replaceUnderScoreWithSpace(productDetails?.tps_check_status) || '--',
            displayKey: 'TPS Check',
            subValue: null
        },
        {
            property: 'mps_check',
            value: replaceUnderScoreWithSpace(productDetails?.mps_check_status) || formatDate(productDetails?.mps_check_date) || 'No',
            displayKey: 'MPS Check',
            subValue: null
        },
    ]

    // Store compliance details for Paper Trail tab
    const complianceDetailsList = [
        {
            property: 'ip_address',
            value: productDetails?.ip_address || productDetails?.compliance_metadata?.ip_address || '192.168.1.101',
            displayKey: 'IP Address',
            isLink: false
        },
        {
            property: 'user_agent',
            value: productDetails?.user_agent || productDetails?.compliance_metadata?.user_agent || 'Mozilla/5.0 (iPhone; CPU iPhone OS...)',
            displayKey: 'User Agent',
            isLink: true
        },
        {
            property: 'referring_url',
            value: productDetails?.referring_url || productDetails?.compliance_metadata?.referring_url || 'https://example-ad.com',
            displayKey: 'Referring URL',
            isLink: false
        },
        {
            property: 'signup_url',
            value: productDetails?.signup_url || productDetails?.compliance_metadata?.signup_url || 'https://example.com/signup-form',
            displayKey: 'Signup URL',
            isLink: false
        },
    ]

    // Store consent details for Paper Trail tab
    const consentDetailsList = [
        {
            property: 'opt_in_timestamp',
            value: formatDate(productDetails?.opt_in_timestamp || productDetails?.consent_metadata?.opt_in_timestamp || productDetails?.created_at) || '12 Dec 2024',
            displayKey: 'Opt-in Timestamp',
            isLink: false
        },
        {
            property: 'consent_text',
            value: productDetails?.consent_text || productDetails?.consent_metadata?.consent_text || 'I agree to receive marketing from XYZ Ltd...',
            displayKey: 'Consent Text',
            isLink: false
        },
        {
            property: 'consent_method',
            value: replaceUnderScoreWithSpace(productDetails?.consent_method || productDetails?.consent_metadata?.consent_method) || 'Checkbox',
            displayKey: 'Consent Method',
            isLink: false
        },
        {
            property: 'email_consent',
            value: formatDate(productDetails?.email_consent_date || productDetails?.consent_metadata?.email_consent) || '12 Dec 2024',
            displayKey: 'Email Consent',
            isLink: false
        },
        {
            property: 'mobile_consent',
            value: formatDate(productDetails?.mobile_consent_date || productDetails?.consent_metadata?.mobile_consent) || '12 Dec 2024',
            displayKey: 'Mobile Consent',
            isLink: false
        },
        {
            property: 'postal_consent',
            value: formatDate(productDetails?.postal_consent_date || productDetails?.consent_metadata?.postal_consent) || '12 Dec 2024',
            displayKey: 'Postal Consent',
            isLink: false
        },
    ]

    // Store key value pair for Paper Trail tab - Validation Checks
    const paperTrailDataList = [
        {
            property: 'tps_check_status',
            value: replaceUnderScoreWithSpace(productDetails?.tps_check_status) || '--',
            displayKey: 'TPS Status',
            status: productDetails?.tps_check_status,
            subValue: null
        },
        {
            property: 'mps_check_status',
            value: replaceUnderScoreWithSpace(productDetails?.mps_check_status) || '--',
            displayKey: 'MPS Status',
            status: productDetails?.mps_check_status,
            subValue: null
        },
        {
            property: 'hlr_check_status',
            value: replaceUnderScoreWithSpace(productDetails?.hlr_check_status) || '--',
            displayKey: 'HLR Check',
            status: productDetails?.hlr_check_status,
            subValue: null
        },
        {
            property: 'llv_check_status',
            value: replaceUnderScoreWithSpace(productDetails?.llv_check_status) || '--',
            displayKey: 'LLV Check',
            status: productDetails?.llv_check_status,
            subValue: null
        },
        {
            property: 'geo_validation_status',
            value: replaceUnderScoreWithSpace(productDetails?.geo_validation_status) || '--',
            displayKey: 'Geo Validation',
            status: productDetails?.geo_validation_status,
            subValue: null
        },
        {
            property: 'suppression_check_status',
            value: replaceUnderScoreWithSpace(productDetails?.suppression_check_status) || '--',
            displayKey: 'Suppression Check',
            status: productDetails?.suppression_check_status,
            subValue: null
        },
        {
            property: 'gdpr_consent_status',
            value: replaceUnderScoreWithSpace(productDetails?.gdpr_consent_status) || '--',
            displayKey: 'GDPR Consent',
            status: productDetails?.gdpr_consent_status,
            subValue: null
        },
    ]

    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()

        toggleRightSidePanel()
        setProductIndex(index)
        setProductDetails(productC.items[index])
        setViewMode('view')
        setType(productC.items.map(item => item.data_type === 'Consumer' ? 'Consumer' : 'Business'))
    }
    // Store buyers by company ID
    const [buyerByCompanyId, setBuyerByCompanyId] = useState()


    // Search functionality
    const handleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    // Display the request status
    const showMessagee = (status: string, text: string) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    // Filter functionality
    const handleFilter = (key, value, updateCollection, checked) => {
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            if (checked) {
                searchParams.set(key, value)

            } else {
                searchParams.delete(key)
            }

            return { searchParams }

        })
        // updateQueryParam(key, value)
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateProductData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        console.log(requestData, 'requestdata')
        console.log(productC.items[clickedProductIndex].id, requestData, 'productdetail')
        try {
            await request.patch(`products/${productC.items[clickedProductIndex].id}`, requestData)
            updateProductC({ reload: true })
            setUpdateProductData(copy(initialUpdateProductData))
            showMessagee('success', 'Product details updated successfully!')
        } catch (err) {
            // console.error('Failed to update product:', err)
            showMessagee('error', 'Failed to update Product details')
        }
    }

    // Add functionality
    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addProductData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('products', requestData)
            updateProductC({ reload: true })
            setAddProductData(copy(initialAddProductData))
            showMessagee('success', 'Product created successfully.')
        } catch (err) {
            showMessagee('error', 'Failed to create product.')
        }
    }

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`products/${id}`)
            updateProductC({ reload: true })
            showMessagee('success', 'Product Deleted Successfully')
        } catch (err) {
            console.error('Failed to delete product:', err)
            showMessagee('error', 'Failed to delete product')
        }
    }

    // Remove functionality
    const handleRemove = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`products/${id}`)
            updateProductC({ reload: true })
            showMessagee('success', 'Product removed successfully')
        } catch (err) {
            console.error('Failed to remove product:', err)
            showMessagee('error', 'Failed to remove product')
        }
    }

    // Next button functionality inside the right side panel
    function handleNextButton() {
        const newIndex = productIndex + 1
        setProductIndex(newIndex)
        setProductDetails(productC?.items[newIndex])

    }

    // Previous button functionality inside the right side panel
    function handlePrevButton() {
        const newIndex = productIndex - 1
        setProductIndex(newIndex)
        setProductDetails(productC?.items[newIndex])
    }

    // Add button in the right panle
    function onAddUserClick() {
        console.log('add clickd')
        setViewMode('add')
        setActiveTab('')
    }

    // Add keyword functionality
    const handleAddKeyword = async (keywords) => {
        try {
            // Add your API call here to save keywords
            console.log('Adding keywords:', keywords)
            // await request.post('keywords', { keywords })
            toggleKeywordsModal()
            showMessagee('success', 'Keywords added successfully!')
        } catch (err) {
            console.error('Failed to add keywords:', err)
            showMessagee('error', 'Failed to add keywords')
        }
    }

    return <div className='page-container'>
        <StatusText
            text={message}
        />
        <>
            <div className='left-container'>
                <Menubar />
            </div>
            <div className='main-content'>
                <Header
                    title='Products'
                />
                <div className='main-content-body'>
                    <Stats
                        title='Stats'
                        statValues={stats}
                        isDateDropList={false}
                        isDateInput={true}
                    />
                    <div className='table-wrapper'>
                        <div className='table-container'>
                            <TablePageHeader
                                title='Product List'
                                onSearch={handleSearch}
                                // q={queryParams.get('q')}
                                toggleFilterDropList={toggleFilterDropList}
                                showFilterDropList={showFilterDropList}
                                onFilterInputChange={onFilterInputChange}
                                // onAddClick={true}
                                onExportClick={null}
                                // moreOptionVisible
                                showActionButtons
                                buttonText='Export Users'
                                quickFilter={quickFilter}
                                currentFilterData={initialFilterData}
                                collection={productC}
                                applyFilter={applyFilter}
                                sliderFilter={handleFilter}
                                updateData={updateProductData}
                                updateCollection={updateProductC}
                                showMoreOption={showMoreOption}
                                toggleMoreOption={toggleMoreOption}
                            />
                            <Table
                                className='category-table'
                                items={productC.items}
                                onRowClick={onRowClick}
                                columns={columns}
                                controlColumns={[]}
                                loaded={productC.loaded}
                                searchParams={productC.searchParams}
                                collection={productC}
                                updateCollection={updateProductC}
                                selectedIndex={productIndex}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </>

        {/* Right Side Panel */}
        {showRightSidePanel &&
            <div
                className='overlay'
                onClick={() => {
                    toggleRightSidePanel()
                    setProductIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={viewMode === 'view'
                        ? 'Product Details'
                        : viewMode === 'edit'
                            ? 'Edit Product'
                            : viewMode === 'add'
                                ? 'Add Product'
                                : ''
                    }
                    details={productDetails}
                    setDetails={setProductDetails}
                    tabs={tabs}
                    setTabs={setTabs}
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                    label='Product Details'
                    profileImg='/company-img.svg'
                    keyValueDataList={keyValueDataList}
                    keyValueDataListTwo={keyValueDataListTwo}
                    keyValueDataListThree={keyValueDataListThree}
                    paperTrailDataList={paperTrailDataList}
                    complianceDetailsList={complianceDetailsList}
                    consentDetailsList={consentDetailsList}
                    labelTwo='Additional Information'
                    // labelValueData={labelValueData}
                    type={type}
                    buttonOneFunction={viewMode === 'view'
                        ? handlePrevButton
                        : viewMode === 'edit' || viewMode === 'add'
                            ? toggleRightSidePanel
                            : viewMode === 'add'
                                ? ''
                                : ''

                    }
                    buttonTwoFunction={viewMode === 'view'
                        ? handleNextButton
                        : viewMode === 'edit' && activeTab === 'user'
                            ? onAddUserClick
                            : viewMode === 'edit'
                                ? handleUpdate
                                : viewMode === 'add'
                                    ? handleAdd
                                    : ''

                    }
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Product'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : viewMode === 'edit' && activeTab === 'user'
                                ? ''
                                : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Product'
                            : viewMode === 'edit' && activeTab === 'user'
                                ? 'Add User'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Send Invite'
                                        : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    stats={{bar: '100',
                        likes: '100',
                        rating: '100'
                    }}
                    // totalDisputes={disputeDetails}
                    // disputesKeyValue={disputesKeyValue[0]}
                    onSearch={handleSearch}
                    toggleTeamModal={toggleTeamModal}
                    // setTeamDetails={setTeamDetails}
                    setIndex={setProductIndex}
                    index={productIndex}
                    collection={productC}
                    usersByCompanyId={buyerByCompanyId}
                    // purchasesKeyValue={purchasesKeyValue[0]}
                    // totalPurchase={purchaseDetails}
                    // updateCollectionOne={updateDisputeC}
                    // updateCollectionTwo={updatePurchaseC}
                    updateData={
                        viewMode === 'edit'
                            ? updateProductData
                            : viewMode === 'add'
                                ? addProductData
                                : ''
                    }
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateProductDataInputChange
                            : viewMode === 'add'
                                ? onAddProductDataInputChange
                                : ''
                    }
                    handleUpdate={handleUpdate}
                    onAddDataInputChange={onAddProductDataInputChange}
                    addData={addProductData}
                    setUpdateData={viewMode === 'edt'
                        ? setUpdateProductData
                        : viewMode === 'add'
                            ? setAddProductData
                            : ''
                    }
                    viewDetailsBtn={true}
                    summaryView={false}
                    page='product'
                    toggleDeleteModal={toggleDeleteModal}
                    deleteModalDescription={setDeleteModalDescription}
                    deleteModalTitle={setDeleteModalTitle}
                    deleteId={buyerByCompanyId}
                    setDeleteBtn={setDeleteBtn}
                    showKeywordsModal={showKeywordsModal}
                    toggleKeywordsModal={toggleKeywordsModal}
                    handleAddKeyword={handleAddKeyword}

                />
            </div>
        }
        {
            showDeleteModal && <Modal
                title={deleteModalTitle}
                toggleModal={toggleDeleteModal}
            >
                <DeleteModal
                    toggleDeleteModal={toggleDeleteModal}
                    handleDelete={handleDelete}
                    buyerByCompanyId={buyerByCompanyId}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }
    </div> }