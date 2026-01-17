'use client'
import { useState, useRef } from 'react'
import Link from 'next/link'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import useFilter from '@/hooks/useFilter'
import { useForm } from '@/hooks/useForm'

import { formatDateTime, getCollectionSearchParamsFromPage, replaceUnderScoreWithSpace } from '@/helpers'
import { copy, shortenText } from '@/helpers'
import useRequest from '@/hooks/useRequest'
import Stats from '@/components/stats'
import Tabs from '@/components/tabs'

import '@/css/pages/billing.css'

const initialFilterData = {
    f_status: {
        operator: 'equals',
        value: '',
        type: 'checkbox'
    },
    f_connection_status: {
        operator: 'equals',
        value: '',
        type: 'checkbox'
    }
}

const stats = [
    {
        mainLabel: 'Leads Due',
        mainValue: '6000',
        subLabel: 'Delivery Completion Rate',
        subValue: '77.5%',
        isActive: true
    },
    {
        mainLabel: 'Leads Delivered',
        mainValue: '4,650',
        subLabel: 'Leads Pending',
        subValue: '1,350',
        isActive: true
    },
    {
        mainLabel: 'Orders Behind Schedule',
        mainValue: '3',
        subLabel: 'Expired',
        subValue: '6',
        isActive: true
    },
    {
        mainLabel: 'API Disconnected',
        mainValue: '5',
        subLabel: 'Buyer / Seller',
        subValue: '3 / 2',
        isActive: true
    },
]

export default function LiveLeads() {
    const { request } = useRequest()

    const [url, setUrl] = useState('admin/live-lead-orders')

    const [liveLeadOrdersC, updateLiveLeadOrdersC] = useCollection(url, getCollectionSearchParamsFromPage())

    // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData
    ] = useFilter(initialFilterData, updateLiveLeadOrdersC)

    // Pass values to the main table
    const [liveLeadOrdersColumns, setLiveLeadOrdersColumns] = useState([
        {
            name: 'Order ID',
            id: 'order_code',
            visible: true,
            sortable: 'backend',
            render: row => <div className='transaction-id'>{row.order_code}</div>
        },
        {
            name: 'Product',
            id: 'product_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.product_details?.name || 'N/A'}
            </div>
        },
        {
            name: 'Ordered On',
            id: 'ordered_on',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>
                {row.ordered_on ? formatDateTime(row.ordered_on) : 'N/A'}
            </div>
        },
        {
            name: 'Leads Ordered',
            id: 'leads_ordered',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.leads_ordered?.toLocaleString() || 'N/A'}
            </div>
        },
        {
            name: 'Connection Status',
            id: 'connection_status',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {replaceUnderScoreWithSpace(row.connection_status) || 'N/A'}
            </div>
        },
        {
            name: 'Schedule',
            id: 'schedule',
            visible: true,
            sortable: false,
            render: row => <div className='category-id'>
                {row.delivery_schedules && row.delivery_schedules.length > 0 ? (
                    <Link href='#' className='link-text'>view schedule</Link>
                ) : (
                    'N/A'
                )}
            </div>
        },
        {
            name: 'Criteria',
            id: 'criteria',
            visible: true,
            sortable: false,
            render: row => <div className='category-id'>
                {row.criteria && row.criteria.length > 0 ? (
                    <Link href='#' className='link-text'>view details</Link>
                ) : (
                    'N/A'
                )}
            </div>
        },
        {
            name: 'API Details',
            id: 'api_details',
            visible: true,
            sortable: false,
            render: row => <div className='category-id'>
                {row.api_endpoint_url ? (
                    <Link href='#' className='link-text'>view details</Link>
                ) : (
                    'N/A'
                )}
            </div>
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => {
                const status = row.status
                let statusClass = ''
                let statusText = replaceUnderScoreWithSpace(status)
                
                if (status === 'AWAITING_START_DATE') {
                    statusClass = 'green'
                } else if (status === 'API_NOT_CONNECTED') {
                    statusClass = 'red'
                } else if (status === 'START_DATE_NOT_SET' || status === 'AWAITING_START') {
                    statusClass = 'blue'
                } else if (status === 'ONGOING') {
                    statusClass = 'green'
                } else if (status === 'COMPLETED') {
                    statusClass = 'green'
                } else if (status === 'DISPUTED') {
                    statusClass = 'yellow'
                } else if (status === 'REFUNDED') {
                    statusClass = 'grey'
                } else if (status === 'CHARGEBACK') {
                    statusClass = 'red'
                }

                return <div className={`status-main ${statusClass}`}>
                    {statusText}
                    {status === 'API_NOT_CONNECTED' && (
                        <img src='/exception.svg' style={{ marginLeft: '5px', width: '14px', height: '14px' }} />
                    )}
                </div>
            }
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            sortable: false,
            render: row => <div className='category-id'>
                <Link href='#' className='link-text'>
                    Order Form
                    <img src='/download-icon.svg' style={{ marginLeft: '5px', width: '14px', height: '14px' }} />
                </Link>
            </div>
        },
    ])

    const [queryParams, setQueryParam] = useQueryParams()

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    
    const [orderIndex, setOrderIndex] = useState()
    const [orderDetails, setOrderDetails] = useState()
    const [viewMode, setViewMode] = useState()

    // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view': {
            'pending': {
                label: 'Pending'
            },
            'ongoing': {
                label: 'Ongoing'
            },
            'completed': {
                label: 'Completed'
            },
            'disputed': {
                label: 'Disputed'
            },
            'refunded': {
                label: 'Refunded'
            },
            'chargeback': {
                label: 'Chargeback'
            },
        },
        'edit': {
            // No tabs for edit mode
        }
    })

    const [activeTab, setActiveTab] = useState('pending')

    const orderDetailsKeyValue = [
        {
            property: 'order_code',
            displayKey: 'Order ID',
            value: orderDetails?.order_code
        },
        {
            property: 'product',
            displayKey: 'Product',
            value: orderDetails?.product_details?.name || 'N/A'
        },
        {
            property: 'ordered_on',
            displayKey: 'Ordered On',
            value: orderDetails?.ordered_on ? formatDateTime(orderDetails.ordered_on) : 'N/A'
        },
        {
            property: 'leads_ordered',
            displayKey: 'Leads Ordered',
            value: orderDetails?.leads_ordered?.toLocaleString() || 'N/A'
        },
        {
            property: 'connection_status',
            displayKey: 'Connection Status',
            value: orderDetails?.connection_status ? replaceUnderScoreWithSpace(orderDetails.connection_status) : 'N/A'
        },
        {
            property: 'status',
            displayKey: 'Status',
            value: orderDetails?.status ? replaceUnderScoreWithSpace(orderDetails.status) : 'N/A'
        },
        {
            property: 'api_endpoint_url',
            displayKey: 'API Endpoint URL',
            value: orderDetails?.api_endpoint_url || 'N/A'
        },
    ]

    const handleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
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
    }

    // Update URL and filter based on active tab
    const handleTabChange = (tabKey) => {
        setActiveTab(tabKey)
        
        // Map tab keys to status values
        const statusMap = {
            'pending': 'AWAITING_START_DATE',
            'ongoing': 'ONGOING',
            'completed': 'COMPLETED',
            'disputed': 'DISPUTED',
            'refunded': 'REFUNDED',
            'chargeback': 'CHARGEBACK'
        }

        const statusValue = statusMap[tabKey]
        
        updateLiveLeadOrdersC(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            if (statusValue) {
                searchParams.set('f_status', statusValue)
            } else {
                searchParams.delete('f_status')
            }
            return { searchParams }
        })
    }

    function handleNextButton() {
        const newIndex = orderIndex + 1
        setOrderIndex(newIndex)
        setOrderDetails(liveLeadOrdersC?.items[newIndex])
    }

    function handlePrevButton() {
        const newIndex = orderIndex - 1
        setOrderIndex(newIndex)
        setOrderDetails(liveLeadOrdersC?.items[newIndex])
    }

    return <div className='page-container'>
        <>
            <div className='left-container'>
                <Menubar />
            </div>
            <div className='main-content'>
                <Header
                    title='Sales - Live Leads'
                />
                <div className='main-content-body'>
                    <Stats
                        title='Stats'
                        statValues={stats}
                        isDateDropList={true}
                        isDateInput={false}
                    />
                    <div className='table-wrapper'>
                        <div className='table-tabs'>
                            <Tabs
                                tabs={tabs['view']}
                                setTabs={setTabs}
                                activeTab={activeTab}
                                setActiveTab={handleTabChange}
                            />
                            <hr className='light-line'/>
                        </div>
                        <TablePageHeader
                            title='Live Leads Orders'
                            onSearch={handleSearch}
                            toggleFilterDropList={toggleFilterDropList}
                            showFilterDropList={showFilterDropList}
                            onFilterInputChange={onFilterInputChange}
                            onAddClick={true}
                            onExportClick={null}
                            showActionButtons
                            buttonText='Export Orders'
                            currentFilterData={initialFilterData}
                            collection={liveLeadOrdersC}
                            applyFilter={applyFilter}
                            sliderFilter={handleFilter}
                            updateData={null}
                            updateCollection={updateLiveLeadOrdersC}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={liveLeadOrdersC.items}
                                columns={liveLeadOrdersColumns}
                                controlColumns={[]}
                                loaded={liveLeadOrdersC.loaded}
                                searchParams={liveLeadOrdersC.searchParams}
                                collection={liveLeadOrdersC}
                                selectedIndex={orderIndex}
                                updateCollection={updateLiveLeadOrdersC}
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
                    setOrderIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title='Live Lead Order Details'
                    details={orderDetails}
                    setDetails={setOrderDetails}
                    labelValueData={orderDetailsKeyValue}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Order'
                        : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Order'
                            : ''
                    }
                    buttonOneFunction={viewMode === 'view'
                        ? handlePrevButton
                        : ''
                    }
                    buttonTwoFunction={viewMode === 'view'
                        ? handleNextButton
                        : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    onSearch={handleSearch}
                    setIndex={setOrderIndex}
                    index={orderIndex}
                    collection={liveLeadOrdersC}
                    viewDetailsBtn={true}
                    summaryView={false}
                    showDropDown={showDropDown}
                    toggleDropDown={toggleDropDown}
                    page='live-leads'
                />
            </div>
        }
    </div>
}

