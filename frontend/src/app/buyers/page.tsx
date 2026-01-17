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
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

const stats = [
    {
        mainLabel: 'Total Buyers',
        mainValue: '2346',
        subLabel: 'Waiting for approval',
        subValue: '12 buyers',
        isActive: true
    },
    {
        mainLabel: 'Total Purchase',
        mainValue: '€12,800',
        subLabel: 'Avg purchase',
        subValue: '€51.20/buyer',
        isActive: true

    },
    {
        mainLabel: 'Total Disputes',
        mainValue: '27',
        subLabel: 'Avg resolution time',
        subValue: '2 days',
        isActive: true

    },
    {
        mainLabel: 'Total Order',
        mainValue: '324',
        subLabel: 'Cancelled order',
        subValue: '17',
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
        value:'',
        type: 'checkbox'
    }
}

// Form initial Data
const initialUpdateBuyerData = {
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
    country:'',
    place: ''
}

// Form initial Data
const initialAddBuyerData = {
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

export default function Buyer() {
    const { request } = useRequest()
    
    // Used to toggle RightSidePanle, FilterDropList , TeamDetailsModal, DeleteModal
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showTeamModal, toggleTeamModal] = useToggle()
    const [showDeleteModal,  toggleDeleteModal] = useToggle()
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
                <div title={row?.email} className='email-sub-text'>
                    {shortenText(row?.email)}
                </div>
            </div>
        },
        {
            name: 'Purchases',
            id: 'total_purchases',
            visible: true,
            sortable: 'backend',
            render: row => <div className='purchases'>
                {row?.total_purchases}
            </div>
        },
        {
            name: 'Disputed',
            id: 'total_disputes',
            visible: true,
            sortable: 'backend',
            render: row => <div className='disputed'>
                <div className='disputes'>
                    {row?.total_disputes}
                </div>
            </div>
        },
        {
            name: 'Status',
            id: 'approval_status',
            visible: true,
            sortable: 'backend',
            render: row => <div 
                title={replaceUnderScoreWithSpace(row?.company_details?.approval_status)}
                className={`status-main ${
                    row?.company_details?.approval_status === 'APPROVED'
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
                        className={`status-no-bg ${
                            row?.company_details?.approval_status === 'APPROVED'
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
                        {shortenText( row?.company_details?.approval_status === 'APPROVED' 
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
                            setClickedBuyerIndex(index)
                            setActiveTab('basic_details')
                            setUpdateBuyerData({
                                first_name: row.name,
                                last_name: row.name,
                                email:row.email,
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

    // Pass values to the team table
    const [teamColumns, setTeamColumns] = useState([
        {
            name: 'Name',
            id: 'name',
            visible: true,
            // sortable: 'backend',
            render: row => <div className='name'>
                {row?.name}
            </div>
        },
        {
            name: 'Email',
            id: 'email',
            visible: true,
            // sortable: 'backend',
            render: row => <div className='email'>
                {row.email}
            </div>
        },
        {
            name: 'Phone',
            id: 'phone',
            visible: true,
            // sortable: 'backend',
            render: row => <div className='phone'>
                <div className='phone'>
                    {row?.company_details?.phone}
                </div>
            </div>
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            // sortable: 'backend',
            render: row => <div className={`status ${
                row?.user_status === 'ACTIVE' 
                    ? 'green' 
                    : row?.user_status === 'PENDING'
                        ? 'yellow'
                        : 'grey'
            }`}>
                {row?.user_status}
            </div>
        },
    ])

    // Set query params
    const [queryParams, setQueryParam, updateQueryParam] = useQueryParams()

    // Stores Buyers data
    const [buyersC, updateBuyersC] = useCollection('admin/buyers', null, null)

    // Stores Buyers data for team Details
    const [teamC, updateTeamC] = useCollection('admin/buyers', null, null)

    // Stores Disputes Collection
    const [disputeC, updateDisputeC] = useCollection('admin/disputes', null, null)

    // Stores Order Collection (quering order api insted of purchase api)
    const [purchaseC, updatePurchaseC] = useCollection('admin/orders', null, null)

    // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData 
    ] = useFilter(initialFilterData, updateBuyersC)

    const [
        addBuyerData,
        setAddBuyerData,
        onAddBuyerDataInputChange,
        addBuyerDataErrors,
        setAddBuyerDataErrorsMap,
        addBuyerDataErrorMessage,
        setAddBuyerDataErrorMessage,
    ] = useForm(copy(initialAddBuyerData))

    // Create the form for editng the buyer Data
    const [
        updateBuyerData,
        setUpdateBuyerData,
        onUpdateBuyerDataInputChange,
        updateBuyerDataErrors,
        setUpdateBuyerDataErrorsMap,
        updateBuyerDataErrorMessage,
        setUpdateBuyerDataErrorMessage,
    ] = useForm(copy(initialUpdateBuyerData))

    // Store the clicked buyer from table row click
    const [buyerDetails, setBuyerDetails] = useState()

    // Store Team Details
    const [teamDetails, setTeamDetails] = useState()

    // Store Each Dispute details
    const [disputeDetails, setDisputeDetails] = useState() 

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    // Store Each Dispute details
    const [purchaseDetails, setPurchaseDetails] = useState() 

    // Clicked Buyer Index
    const [clickedBuyerIndex, setClickedBuyerIndex] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [buyerIndex, setBuyerIndex] = useState()

    // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view':{
            'basic_details': {
                label: 'Basic Details'
            },
            'disputes': {
                label: 'Disputes'
            },
            'purchases': {
                label: 'Purchases'
            },
            'activity_log': {
                label: 'Activity log'
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

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()
 
    // Sets the active tab when user clicks on 
    // it by defail 'basic_details' will be the tab selected
    const [activeTab, setActiveTab] = useState('basic_details')

    const [message, setMessage] = useState([])

    // Store key value pair to pass into KeyValue Compoennt
    const keyValueDataList = [
        {
            property: 'address',
            value: buyerDetails?.notes || 'N/A',
            displayKey: 'Address'

        },
        {
            property: 'ico-no',
            value: buyerDetails?.company_details?.ico_number || 'N/A',
            displayKey: (
                <div className='key-with-img'>
                    ICO No {buyerDetails?.company_details?.ico_number 
                        ? '' 
                        : <img className='cross-icon' src='/cross.svg'/>
                    } 
                </div>
            )

        },
        {
            property: 'vat-no',
            value: buyerDetails?.company_details?.vat_number || 'N/A',
            displayKey:(
                <div className='key-with-img'>
                    Vat No {buyerDetails?.company_details?.vat_number 
                        ? '' 
                        : <img className='cross-icon' src='/cross.svg' />
                    }
                </div>
            )

        },
        {
            property: 'company_status',
            value: buyerDetails?.company_details?.status || 'N/A',
            displayKey: 'Company Status'

        },
        {
            property: 'gdpr_fine',
            value: buyerDetails?.company_details?.gdpr_fines ? 'Yes' : 'No',
            displayKey: 'GDPR Fines'

        },
        {
            property: 'total_spent',
            value: buyerDetails?.company_details?.total_spent || '0',
            displayKey: 'Total Spent '

        },
    ]

    // Store key value pair to pass into KeyValue Compoennt
    const disputesKeyValue = disputeDetails?.map((item) => (
    [
        {
            property: 'raised_on',
            value: formatDateTime(item?.raised_date) || 'N/A',
            displayKey: 'Raised On'

        },
        {
            property: 'product_name',
            value: item?.product_name || 'N/A',
            displayKey: 'Product Name'

        },
        {
            property: 'purchase_id',
            value: item?.purchase_id || 'N/A',
            displayKey: 'Purchase ID'

        },
        {
            property: 'seller',
            value: item?.id_seller || 'N/A',
            displayKey: 'Seller'

        },
        {
            property: 'paid_amount',
            value: item?.disputed_amount || 'N/A',
            displayKey: 'Paid Amount'
        },
    ]))

    // Store key value pair to pass into KeyValue Compoennt
    const purchasesKeyValue = purchaseDetails?.map((item) => (
        [
            {
                property: 'purchased_on',
                value: formatDateTime(item?.buyer_details?.first_purchase_date) || 'N/A',
                displayKey: 'Purchased on'

            },
            {
                property: 'purchase_amount',
                value: item?.total_amount || 'N/A',
                displayKey: 'Purchase Amount'

            },
            {
                property: 'seller',
                value: item?.product_details?.name || 'N/A',
                displayKey: 'Seller'

            },
            {
                property: 'dispute_raised',
                value: item?.buyer_details?.total_disputes || 'N/A',
                displayKey: 'Dispute Raised'

            },
        ])) 

    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()
        
        toggleRightSidePanel()
        setBuyerIndex(index)
        setBuyerDetails(buyersC.items[index])
        setViewMode('view')
    }

    // Condtionally add action card button functions
    const actionCardFucntion = async (e, action) => {
        e.preventDefault()
        if (action === 'APPROVED') {
            try {
                await request.delete('buyers/deactivate')
                updateBuyersC({ reload: true })
                showMessagee('success', 'User deactivated successfully.')
            } catch (err) {
                console.error('Failed to add user:', err)
                showMessagee('error', 'Error deactivating user.' )
            }
        }
        if (action === 'PENDING_APPROVAL') {
            try {
                await request.delete('buyers/activate')
                updateBuyersC({ reload: true })
                showMessagee('success', 'User activated successfully.')
            } catch (err) {
                console.error('Failed to add user:', err)
                showMessagee('error', 'Failed to activate user.')
            }
        }
        if (action === 'NOT_VERIFIED') {
            try {
                await request.delete('buyers/resent-activation')
                updateBuyersC({ reload: true })
                showMessagee('success', 'Activation link shared successfully.')

            } catch (err) {
                console.error('Failed to add user:', err)
                showMessagee('error', 'Failed to send activation link.')
            }
        }
    }

    // Store buyers by company ID
    const [buyerByCompanyId, setBuyerByCompanyId] = useState()

    useEffect(() => {
        setBuyerByCompanyId(buyersC.items.filter(item => 
            item.company_details.id === buyerDetails?.company_details?.id
        ))
        setDisputeDetails(disputeC.items.filter(item => 
            item.buyer_details.id === buyerDetails?.id
        ))
        setPurchaseDetails(purchaseC.items.filter(item =>
            item.buyer_details.id === buyerDetails?.id
        ))

    }, [buyerIndex, buyerDetails, viewMode]);

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
        setMessage((prev) => [...prev, {id, status,  text}])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id  !== id))
        }, 5000)
    }

    // Filter functionality
    const handleFilter = (key, value, updateCollection, checked) => {
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            if(checked) {
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
        let requestData = copy(updateBuyerData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        console.log(requestData, 'requestdata')
        console.log(buyersC.items[clickedBuyerIndex].id, requestData, 'buyerdetail')
        try {
            await request.patch(`buyers/${buyersC.items[clickedBuyerIndex].id}`, requestData)
            updateBuyersC({ reload: true })
            setUpdateBuyerData(copy(initialUpdateBuyerData))
            showMessagee('success', 'Buyer details updated successfully!')
        } catch (err) {
            // console.error('Failed to update user:', err)
            showMessagee('error', 'Failed to update Buyer details')
        }
    }

    // Add functionality
    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addBuyerData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateBuyersC({ reload: true })
            setAddBuyerData(copy(initialAddBuyerData))
            showMessagee('success', 'User invite sent successfully.' )
        } catch (err) {
            showMessagee('success', 'Failed to send user invite.')
        }
    }

    // Delete functionality
    const handleDelete = async(e, id) => {
        e.preventDefault()

        try {
            await request.delete(`buyers/${id}`)
            updateBuyersC({ reload: true })
            showMessagee('success', 'Buyer Deleted Successfully' )
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to delete buyer')
        }
    }

    // Remove functionality
    const handleRemove = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`buyers/${id}`)
            updateBuyersC({ reload: true })
            showMessagee('success', 'User removed successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to removed user')
        }
    }

    // Next button functionality inside the right side panel
    function handleNextButton() {
        const newIndex = buyerIndex + 1
        setBuyerIndex(newIndex)
        setBuyerDetails(buyersC?.items[newIndex])

    }

    // Previous button functionality inside the right side panel
    function handlePrevButton() {
        const newIndex = buyerIndex - 1
        setBuyerIndex(newIndex)
        setBuyerDetails(buyersC?.items[newIndex])
    }

    // Add button in the right panle
    function onAddUserClick() {
        console.log('add clickd')
        setViewMode('add')
        setActiveTab('')
    }

    return <div className='page-container'>
        <StatusText
            text={message}
        />
        <>
            <div className='left-container'>
                <Menubar/>
            </div>
            <div className='main-content'>
                <Header
                    title='Buyers'
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
                                title='Buyer List'
                                onSearch={handleSearch}
                                // q={queryParams.get('q')}
                                toggleFilterDropList={toggleFilterDropList}
                                showFilterDropList={showFilterDropList}
                                onFilterInputChange={onFilterInputChange}
                                onAddClick={true}
                                onExportClick={null}
                                // moreOptionVisible
                                showActionButtons
                                buttonText='Export Users'
                                quickFilter={quickFilter}
                                currentFilterData={initialFilterData}
                                collection={buyersC}
                                applyFilter={applyFilter}
                                sliderFilter={handleFilter}
                                updateData={updateBuyerData}
                                updateCollection={updateBuyersC}
                                showMoreOption={showMoreOption}
                                toggleMoreOption={toggleMoreOption}
                            />
                            <Table
                                className='category-table'
                                items={buyersC.items}
                                onRowClick={onRowClick}
                                columns={columns}
                                controlColumns={[]}
                                loaded={buyersC.loaded}
                                searchParams={buyersC.searchParams}
                                collection={buyersC}
                                updateCollection={updateBuyersC}
                                selectedIndex={buyerIndex}
                                enableColumnPreference
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
                    setBuyerIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={viewMode === 'view' 
                        ? 'Buyers Information' 
                        : viewMode === 'edit' 
                            ? 'Edit Buyer'
                            : viewMode === 'add'
                                ? 'Add User'
                                :''
                    }
                    details={buyerDetails}
                    setDetails={setBuyerDetails}
                    tabs={tabs}
                    setTabs={setTabs}
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                    label='Company Details'
                    profileImg='/company-img.svg'
                    keyValueDataList={keyValueDataList}
                    labelTwo='Team Details'
                    // labelValueData={labelValueData}
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
                        ? 'Previous Transaction'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : viewMode === 'edit' && activeTab === 'user'
                                ? ''
                                : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Transaction'
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
                    totalDisputes={disputeDetails}
                    disputesKeyValue={disputesKeyValue[0]}
                    onSearch={handleSearch}
                    toggleTeamModal={toggleTeamModal}
                    setTeamDetails={setTeamDetails}
                    setIndex={setBuyerIndex}
                    index={buyerIndex}
                    collection={buyersC}
                    usersByCompanyId={buyerByCompanyId}
                    purchasesKeyValue={purchasesKeyValue[0]}
                    totalPurchase={purchaseDetails}
                    updateCollectionOne={updateDisputeC}
                    updateCollectionTwo={updatePurchaseC}
                    updateData={
                        viewMode === 'edit' 
                            ? updateBuyerData
                            : viewMode === 'add'
                                ? addBuyerData 
                                : ''
                    }
                    updateOnChange={
                        viewMode === 'edit' 
                            ? onUpdateBuyerDataInputChange
                            : viewMode === 'add'
                                ? onAddBuyerDataInputChange
                                : ''
                    }
                    handleUpdate={handleUpdate}
                    onAddDataInputChange={onAddBuyerDataInputChange}
                    addData={addBuyerData}
                    setUpdateData={viewMode === 'edt' 
                        ? setUpdateBuyerData 
                        : viewMode === 'add' 
                            ? setAddBuyerData 
                            : ''
                    }
                    viewDetailsBtn={true}
                    summaryView={false}
                    page='buyer'
                    toggleDeleteModal={toggleDeleteModal}
                    deleteModalDescription={setDeleteModalDescription}
                    deleteModalTitle={setDeleteModalTitle}
                    deleteId={buyerByCompanyId}
                    setDeleteBtn={setDeleteBtn}
                    
                />
            </div>
        }

        {/* Team Table inside Modal */}
        {showTeamModal && 
            <div className='team-modal'>
                <Modal
                    title='Team Details'
                    toggleModal={toggleTeamModal}
                >
                    <Table 
                        className='team-table'
                        items={buyerByCompanyId}
                        columns={teamColumns}
                        controlColumns={[]}
                        loaded={teamC.loaded}
                        searchParams={teamC.searchParams}
                        collection={buyerByCompanyId}
                        updateCollection={updateTeamC}
                    /> 
                </Modal> 
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
    </div>
}