'use client'

import { useState, useRef, useEffect } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import Stats from '@/components/stats'
import RightSidePanel from '@/components/rightSidePanel'
import Modal from '@/components/modal'

import { formatDateTime, shortenText } from '@/helpers'
import { copy } from '@/helpers'
import { replaceUnderScoreWithSpace } from '@/helpers'

import useRequest from '@/hooks/useRequest'
import useFilter from '@/hooks/useFilter'
import useToggle from '@/hooks/useToggle'
import useQueryParams from '@/hooks/useQueryParams'
import useCollection from '@/hooks/useCollection'
import { useForm } from '@/hooks/useForm'

import '@/css/pages/seller.css'
import StatusText from '@/components/statusText'
import DeleteModal from '@/components/deleteModal'

const stats = [
    {
        mainLabel: 'Total Sellers',
        mainValue: '143',
        subLabel: 'Waiting for approval',
        subValue: '12 sellers',
        isActive: true
    },
    {
        mainLabel: 'Total Listing',
        mainValue: '287',
        subLabel: 'Date / Lead listing',
        subValue: '195 / 92',
        isActive: true

    },
    {
        mainLabel: 'Total Disputes',
        mainValue: '32',
        subLabel: 'Avg resolution time',
        subValue: '3 days',
        isActive: true

    },
    {
        mainLabel: 'Total Sales',
        mainValue: '€752,000',
        subLabel: 'Value in dispute or refund',
        subValue: '14',
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
        mainValue: '€752,000',
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
        label: 'Pending buyers',
        key: 'PENDING',
        isActive: true
    },
    {
        label: 'Rejected/Blocked buyers',
        key: 'INACTIVE',
        isActive: false
    },
    {
        label: 'Dispute raised buyers',
        key: 'NOT_VERIFIED',
        isActive: false
    },
    {
        label: 'Newly signed-up buyers',
        key: 'ACTIVE',
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

const records = [
    {
        name: 'Duplicate',
        value: 0
    },
    {
        name: 'Do not contact',
        value: 0
    },
    {
        name: 'Quality control DNC',
        value: 0
    },
    {
        name: 'Email information empty',
        value: 0
    },
    {
        name: 'Telephone preference service',
        value: 0
    },
    {
        name: 'Corporate telephone preference service',
        value: 0
    },
]

// Form initial Data
const initialUpdateSellerData = {
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
const initialAddSellerData = {
    name: '',
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
export default function Seller() {
    const { request } = useRequest()

    // Used to toggle RightSidePanle, FilterDropList , TeamDetailsModal
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showTeamModal, toggleTeamModal] = useToggle()
    const [showDeleteModal,  toggleDeleteModal] = useToggle()
    const [showFileSummary, toggleFileSummary] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()
    

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'Signed up on',
            id: 'signed_up_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='signed-up'>
                {formatDateTime(row?.company_details?.signed_up_date)}
            </div>
        },
        {
            name: 'Company Name',
            id: 'company_details_.name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='company-details'>
                <div className='company-place'>
                    <img className='country-icon' src='/country.svg' />
                </div>
                <div className='company-details-wrapper'>
                    <button
                        title={row?.company_details?.name}
                        className='company-name'
                    >
                        {shortenText(row?.company_details?.name)}
                    </button>
                    <div className='company-reg-sub-text'>
                        {row?.company_details?.registration_number}
                    </div>
                </div>
            </div>
        },
        {
            name: 'User',
            id: 'name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='user-name'>
                <div className='name'>
                    {row?.name}
                </div>
                <div className='email-sub-text'>
                    {shortenText(row?.email)}
                </div>
            </div>
        },
        {
            name: 'Total Listing',
            id: 'total_listing',
            visible: true,
            sortable: 'backend',
            render: row => <div className='purchases'>
                {row?.total_listings}
            </div>
        },
        {
            name: 'Total Sales',
            id: 'total_sales',
            visible: true,
            sortable: 'backend',
            render: row => <div className='disputed'>
                <div className='disputes'>
                    {row?.total_sales}
                </div>
            </div>
        },
        {
            name: 'Rating',
            id: 'rating',
            visible: true,
            sortable: 'backend',
            render: row => <div className='rating'>
                
                {row.rating && 
                    <img className='star-icon' src='/star.svg' />
                }
                <div>{row.rating ? row.rating : 'N/A'}</div>
            </div>
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                title={replaceUnderScoreWithSpace(row?.company_details?.approval_status)}
                className={`status-main ${row?.company_details?.approval_status === 'APPROVED'
                        ? 'green'
                        : row?.company_details?.approval_status === 'PENDING_APPROVAL'
                            ? 'yellow'
                            : 'grey'
                    }`}
            >
                {shortenText(replaceUnderScoreWithSpace(row?.company_details?.approval_status))}
            </div>
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => <div className='action'>
                <div className='action-card-button'>
                    <button
                        title={row?.company_details?.approval_status === 'APPROVED'
                            ? 'Deactivate'
                            : row?.company_details?.approval_status === 'PENDING_APPROVAL'
                                ? 'Activate'
                                : 'Re-send Activation Link'
                        }
                        className={`status-no-bg ${row?.company_details?.approval_status === 'APPROVED'
                                ? 'red-no-bg'
                                : row?.company_details?.approval_status === 'PENDING_APPROVAL'
                                    ? 'blue-no-bg'
                                    : 'blue-no-bg'
                            }`}
                        onClick={(e) => {
                            e.stopPropagation()
                            actionCardFucntion(e, row?.company_details?.approval_status)
                        }}
                    >
                        {shortenText(row?.company_details?.approval_status === 'APPROVED'
                            ? 'Deactivate'
                            : row?.company_details?.approval_status === 'PENDING_APPROVAL'
                                ? 'Activate'
                                : 'Re-send Activation Link'
                        )}
                    </button>
                </div>
                <div className='action-button'>
                    <button
                        onClick={(e) => {
                            e.stopPropagation()
                            setViewMode('edit')
                            toggleRightSidePanel()
                            setClickedSellerIndex(index)
                            setActiveTab('basic_details')
                            setUpdateSellersData({
                                name: row.name,
                                email: row.email,
                                phone: row?.company_details?.phone,
                                company_name: row?.company_details?.name,
                                total_disputes: row.total_disputes,
                                status: row.status,
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
                                status: row?.status,
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
                            setDeleteModalDescription('Are you sure, want to delete this buyer')
                            setDeleteModalTitle('Delete Buyer')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setSellersByCompanyId(row.id)
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
    const [sellersC, updateSellersC] = useCollection('admin/sellers', null, null)

    // // Stores Disputes Collection
    // const [disputeC, updateDisputeC] = useCollection('admin/disputes', null, null)

    // // Stores Order Collection (quering order api insted of purchase api)
    // const [purchaseC, updatePurchaseC] = useCollection('admin/orders', null, null)

    // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData
    ] = useFilter(initialFilterData, updateSellersC)

    const [
        addSellersData,
        setAddSellersData,
        onAddSellersDataInputChange,
        addSellersDataErrors,
        setAddSellersDataErrorsMap,
        addSellerDataErrorMessage,
        setAddSellerDataErrorMessage,
    ] = useForm(copy(initialAddSellerData))

    // Create the form for editng the buyer Data
    const [
        updateSellersData,
        setUpdateSellersData,
        onUpdateSellersDataInputChange,
        updateSellersDataErrors,
        setUpdateSellersDataErrorsMap,
        updateSellersDataErrorMessage,
        setUpdateSellerDataErrorMessage,
    ] = useForm(copy(initialUpdateSellerData))

    // Store the clicked buyer from table row click
    const [sellerDetails, setSellerDetails] = useState()

    // // Store Each Dispute details
    // const [disputeDetails, setDisputeDetails] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    // Store Each Dispute details
    const [purchaseDetails, setPurchaseDetails] = useState()

    // Clicked Buyer Index
    const [clickedSellerIndex, setClickedSellerIndex] = useState()

    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [sellerIndex, setSellerIndex] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    const [message, setMessage] = useState([])


    // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view': {
            'basic_details': {
                label: 'Basic Details'
            },
            'listing': {
                label: 'Listing'
            },
            'activity_log': {
                label: 'Activity log'
            },
            'performance': {
                label: 'Performance'
            },
        },
        'edit': {
            'basic_details': {
                label: 'Basic Details'
            },
            'user': {
                label: 'User'
            },
        }
    })

    // Sets the active tab when user clicks on 
    // it by defail 'basic_details' will be the tab selected
    const [activeTab, setActiveTab] = useState('basic_details')

    // Store hardcoded perfomance tab hey value need to change
    // this to dynamic value
    const performanceKeyValue = [
        {
            property: 'leads_sold',
            value: '412,567',
            displayKey: 'Leads Sold'
        },
        {
            property: 'acceptance_rate',
            value: '97.2%',
            displayKey: 'Acceptence Rate'
        },
        {
            property: 'dispute_rate',
            value: '1.8%',
            displayKey: 'Dispute Rate'
        },
        {
            property: 'forwarding_success',
            value: '94.5%',
            displayKey: 'Forwarding Success'
        },
        {
            property: 'tps',
            value: '99%',
            displayKey: 'TPS%'
        },
        {
            property: 'score',
            value: '92',
            displayKey: 'Score'
        },
    ]
    
    // Store key value pair to pass into KeyValue Compoennt
    const keyValueDataList = [
        {
            property: 'address',
            value: sellerDetails?.notes || 'N/A',
            displayKey: (<div className='key-with-img'>
                Address {sellerDetails?.notes
                    ? ''
                    : <img className='cross-icon' src='/cross.svg' />
                }
            </div>)

        },
        {
            property: 'ico-no',
            value: sellerDetails?.company_details?.ico_number || 'N/A',
            displayKey: (
                <div className='key-with-img'>
                    ICO No {sellerDetails?.company_details?.ico_number
                        ? ''
                        : <img className='cross-icon' src='/cross.svg' />
                    }
                </div>
            )

        },
        {
            property: 'vat-no',
            value: sellerDetails?.company_details?.vat_number || 'N/A',
            displayKey: (
                <div className='key-with-img'>
                    Vat No {sellerDetails?.company_details?.vat_number
                        ? ''
                        : <img className='cross-icon' src='/cross.svg' />
                    }
                </div>
            )

        },
        {
            property: 'company_status',
            value: sellerDetails?.company_details?.status || 'N/A',
            displayKey: 'Company Status'

        },
        {
            property: 'gdpr_fine',
            value: sellerDetails?.company_details?.gdpr_fines ? 'Yes' : 'No',
            displayKey: 'GDPR Fines'

        },
        {
            property: 'seller_followers',
            value: sellerDetails?.company_details?.follower_count || '0',
            displayKey: 'Total Spent '

        },
    ]

    // Store key value pair to pass into KeyValue Compoennt
    const labelValueData = [
        {
            property: 'name',
            value: sellerDetails?.email,
            displayKey: sellerDetails?.name
            
        },
        {
            property: 'phone',
            value: sellerDetails?.company_details?.phone,
            displayKey: 'Phone'

        },
        {
            property: 'position',
            value: sellerDetails?.position,
            displayKey: 'Position'
        }
    ];

    // Store key value pair to pass into KeyValue Compoennt
    const disputesKeyValue = sellersC.items?.map((item) => (
        [
            {
                property: 'name',
                value: item.name || 'N/A',
                displayKey: 'Name'

            },
            {
                property: 'position',
                value: item?.position|| 'N/A',
                displayKey: 'Product Name'

            },
            {
                property: 'follower_count',
                value: item?.purchase_id || 'N/A',
                displayKey: 'Purchase ID'

            },
            {
                property: 'total_sale',
                value: item?.company_details?.total_sales || 'N/A',
                displayKey: 'Seller'

            },
            {
                property: 'rating',
                value: item?.rating || 'N/A',
                displayKey: 'Paid Amount'
            },
    ]))

    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()

        toggleRightSidePanel()
        setSellerIndex(index)
        setSellerDetails(sellersC.items[index])
        setViewMode('view')
    }

    // Store buyers by company ID
    const [sellerByCompanyId, setSellerByCompanyId] = useState()

    useEffect(() => {
        setSellerByCompanyId(sellersC.items.filter(item =>
            item.company_details.id === sellerDetails?.company_details?.id
        ))
        // setDisputeDetails(disputeC.items.filter(item =>
        //     item.buyer_details.id === buyerDetails?.id
        // ))
        // setPurchaseDetails(purchaseC.items.filter(item =>
        //     item.buyer_details.id === buyerDetails?.id
        // ))

    }, [sellerIndex, sellerDetails, viewMode]);

    // Search functionality
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
        // updateQueryParam(key, value)
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateSellersData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        try {
            await request.patch(`sellers/${sellersC.items[clickedSellerIndex].id}`, requestData)
            updateSellersC({ reload: true })
            setUpdateSellersData(copy(initialUpdateSellerData))
            showMessage('success', 'User details updated successfully!')
        } catch (err) {
            console.error('Failed to update user:', err)
            showMessage('error', 'Failed to update User details')
        }
    }

    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addSellersData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('sellers', requestData)
            updateSellersC({ reload: true })
            setAddSellersData(copy(initialAddSellerData))
            showMessage('success', 'Successfully added a user')
        } catch (err) {
            // console.error('Failed to add user:', err)
            // alert('Failed to add user')
            showMessage('error',  'failed to add user')
        }
    }

    const actionCardFucntion = async (e, action) => {
        e.preventDefault()
        if (action === 'APPROVED') {
            try {
                await request.delete('buyers/deactivate')
                updateSellersC({ reload: true })
                showMessage('success', 'User deactivated successfully.')


            } catch (err) {
                console.error('Failed to add user:', err)
                showMessage('error', 'Error deactivating user.')
            }
        }
        if (action === 'PENDING_APPROVAL') {
            try {
                await request.delete('buyers/activate')
                updateSellersC({ reload: true })
                showMessage('success', 'User activated successfully.')


            } catch (err) {
                console.error('Failed to add user:', err)
                showMessage('error', 'Failed to activate user.')

            }
        }
        if (action === 'NOT_VERIFIED') {
            try {
                await request.delete('buyers/resent-activation')
                updateSellersC({ reload: true })
                showMessage('success', 'Activation link shared successfully.')

            } catch (err) {
                console.error('Failed to add user:', err)
                showMessage('error', 'Failed to send activation link.')
            }
        }
    }

    // Display the request status
    const showMessage = (status: string, text: string) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`buyers/${id}`)
            updateSellersC({ reload: true })
            showMessage('success', 'Seller Deleted Successfully')


        } catch (err) {
            console.error('Failed to add user:', err)
            showMessage('error', 'Failed to delete Seller')
        }
    }

    function handleNextButton() {
        const newIndex = sellerIndex + 1
        setSellerIndex(newIndex)
        setSellerDetails(sellersC?.items[newIndex])

    }

    function handlePrevButton() {
        const newIndex = sellerIndex - 1
        setSellerIndex(newIndex)
        setSellerDetails(sellersC?.items[newIndex])
    }
    
    // Add button in the right panle
    function onAddUserClick() {
        console.log('add clickd')
        setViewMode('add')
        setActiveTab('')
    }

    // Remove functionality
    const handleRemove = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`sellers/${id}`)
            updateSellersC({ reload: true })
            showMessage('success', 'User removed successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessage('error', 'Failed to removed user')
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
                    title='Sellers'
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
                                title='Sellers List'
                                onSearch={handleSearch}
                                // q={queryParams.get('q')}
                                toggleFilterDropList={toggleFilterDropList}
                                showFilterDropList={showFilterDropList}
                                onFilterInputChange={onFilterInputChange}
                                onAddClick={true}
                                onExportClick={null}
                                // moreOptionVisible
                                quickFilter={quickFilter}
                                buttonText='Export Users'
                                currentFilterData={initialFilterData}
                                collection={sellersC.items}
                                applyFilter={applyFilter}
                                sliderFilter={handleFilter}
                                updateCollection={updateSellersC}
                                showMoreOption={showMoreOption}
                                toggleMoreOption={toggleMoreOption}
                                showActionButtons
                            />
                            <Table
                                className='category-table'
                                items={sellersC.items}
                                onRowClick={onRowClick}
                                columns={columns}
                                controlColumns={[]}
                                loaded={sellersC.loaded}
                                searchParams={sellersC.searchParams}
                                collection={sellersC}
                                updateCollection={updateSellersC}
                                selectedIndex={sellerIndex}
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
                    setSellerIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={viewMode === 'view'
                        ? 'Seller Information'
                        : viewMode === 'edit'
                            ? 'Edit Seller'
                            : viewMode === 'add'
                                ? 'Add User'
                                : ''
                    }
                    details={sellerDetails}
                    setDetails={setSellerDetails}
                    tabs={tabs}
                    setTabs={setTabs}
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                    label='Company Details'
                    profileImg='/company-img.svg'
                    keyValueDataList={keyValueDataList}
                    labelTwo='User Details'
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Seller'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : viewMode === 'edit' && activeTab === 'user'
                                ? ''
                                : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Seller'
                            : viewMode === 'edit' && activeTab === 'user'
                                ? 'Add User'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Send Invite'
                                        : ''
                    }
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
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    totalDisputes={[sellerDetails]}
                    disputesKeyValue={disputesKeyValue[0]}
                    onSearch={handleSearch}
                    toggleTeamModal={toggleTeamModal}
                    setIndex={setSellerIndex}
                    index={sellerIndex}
                    collection={sellersC}
                    usersByCompanyId={labelValueData}
                    totalPurchase={purchaseDetails}
                    records={records}
                    updateData={updateSellersData}
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateSellersDataInputChange
                            : viewMode === 'add'
                                ? onAddSellersDataInputChange
                                : ''
                    }
                    handleUpdate={handleUpdate}
                    onAddDataInputChange={onAddSellersDataInputChange}
                    addData={addSellersData}
                    setUpdateData={setUpdateSellersData}
                    viewDetailsBtn={false}
                    summaryView={true}
                    page='seller'
                    performaceKeyValue={performanceKeyValue}
                    toggleFileSummary={toggleFileSummary}
                    showFileSummary={showFileSummary}
                    toggleDeleteModal={toggleDeleteModal}
                    deleteModalDescription={setDeleteModalDescription}
                    deleteModalTitle={setDeleteModalTitle}
                    deleteId={sellerByCompanyId}
                    setDeleteBtn={setDeleteBtn}
                />
            </div>
        }
        {
            showDeleteModal && <Modal
                title='Delete Buyer'
                toggleModal={toggleDeleteModal}
            >
                <DeleteModal
                    toggleDeleteModal={toggleDeleteModal}
                    handleDelete={deleteBtn === 'Delete' ? handleDelete : handleRemove}
                    buyerByCompanyId={sellerByCompanyId}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }
    </div>
}