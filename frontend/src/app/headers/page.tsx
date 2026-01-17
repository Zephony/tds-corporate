'use client'
import { useState, useRef } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'

import { getCollectionSearchParamsFromPage } from '@/helpers'
import { copy } from '@/helpers'
import useRequest from '@/hooks/useRequest'

// Form initial Data
const initialUpdateHeaderData = {
    data_type: '',
    category_name: '',
    img: '',
    status: '',
}

// Form initial Data
const initialAddHeaderData = {
    data_type: '',
    category_name: '',
    img: '',
    status: '',
}

export default function Headers() {

    const { request } = useRequest()

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'S.No',
            id: 'sno',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{row.id}</div>
        },
        {
            name: 'Data Type',
            id: 'data-type',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type'>{row.name}</div>
        },
        {
            name: 'Category Name',
            id: 'category-name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='category-img'>
                    <img src='/demo-icon.svg'></img>
                </div>
                <div className='name'>
                    {row.name}
                </div>
            </div>
        },
        {
            name: 'Category ID',
            id: 'category-id',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>{row.id_data_type}</div>
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => <div className='status-main'>
                <div className={`status-${row.status}`}>
                    {row.status}
                </div>
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
                            setHeaderDetail(headerC.items[index])
                            setUpdateHeaderData({
                                data_type: row.name,
                                category_name: row.name,
                                img: '/demo-icon.svg',
                                status: row.status,
                            })
                            toggleRightSidePanel()
                        }}
                        className='edit-icon-wrapper'
                    >
                        <img
                            className='edit-icon'
                            src='/edit-icon.svg'
                        />
                    </button>
                    <button className='delete-icon-wrapper'>
                        <img
                            className='delete-icon'
                            src='/delete-icon.svg'
                        />
                    </button>
                </div>

            </div>
        },
    ])

    const [queryParams, setQueryParam] = useQueryParams()
    const [headerC, updateHeaderC] = useCollection('admin/categories', getCollectionSearchParamsFromPage())

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()


    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [headerIndex, setHeaderIndex] = useState()

    const [selectedDocument, setSelectedDocument] = useState([])
    const [uploadedFile, setUploadedFile] = useState()

    const [
        addHeaderData,
        setAddHeaderData,
        onAddHeaderDataInputChange,
        addHeaderDataErrors,
        setAddHeaderDataErrorsMap,
        addHeaderDataErrorMessage,
        setAddHeaderDataErrorMessage,
    ] = useForm(copy(initialAddHeaderData))


    // Create the form for editng the buyer Data
    const [
        updateHeaderData,
        setUpdateHeaderData,
        onUpdateHeaderDataInputChange,
        updateHeaderDataErrors,
        setUpdateHeaderDataErrorsMap,
        updateHeaderDataErrorMessage,
        setUpdateHeaderDataErrorMessage,
    ] = useForm(copy(initialUpdateHeaderData))

    // Store the clicked buyer from table row click
    const [headerDetails, setHeaderDetail] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    const fileInputRef = useRef()
    console.log(queryParams, 'q and queryparams')

    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addHeaderData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateHeaderC({ reload: true })
            setAddHeaderData(copy(initialAddHeaderData))
        } catch (err) {
            console.error('Failed to add user:', err)
            alert('Failed to add user')
        }
    }

    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateHeaderC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    // File Upload Function
    const handleDropFile = async (files) => {
        const reader = new FileReader()
        reader.onloadend = () => {
            const newId = selectedDocument.length + 1
            const newDocument = {
                id: newId,
                src: reader.result,
                alt: `Image${newId}`,
                type: files.type.startsWith('pdf')
                    ? 'pdf'
                    : 'image',
                name: files.name,
            }

            setSelectedDocument([newDocument])
        }
        fileInputRef.current.value = '';
        reader.readAsDataURL(files)

        // Upload immediately after reading the file
        const formData = new FormData();
        formData.append('file', files);
        formData.append('description', 'nnnnn');
        try {
            const [status, data] = await request.postFormFiles('transduction-task-files', formData)
            console.log(data, status, 'Uploaded successfully');
            setUploadedFile(data.data)
        } catch (err) {
            console.log('Upload error', err);
        }
    }

    const handleFileUpload = (e) => {
        const files = e.target.files[0]
        if (files) handleDropFile(files)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        const file = e.dataTransfer.files[0]
        if (file) handleDropFile(file)
    }

    const handleDragOver = (e) => {
        e.preventDefault()
    }

    // Click Function that reffer the input click when clicked on the browse button
    const handleAddClick = () => {
        console.log('clicked')
        // Open the file picker
        fileInputRef.current.value = '';
        fileInputRef.current.click()
    }

    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()

        setHeaderIndex(index)
        setHeaderDetail(headerC.items[index])
        setViewMode('view')
    }

    return <div className='page-container'>
        <>
            <div className='left-container'>
                <Menubar
                />
            </div>
            <div className='main-content'>
                <Header
                    title='Categorization'
                />
                <div className='main-content-body'>
                    <div className='table-wrapper'>
                        <TablePageHeader
                            title='TDS Headers'
                            onSearch={handleSearch}
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            onMoreOptionClick={true}
                            buttonText='Add'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={headerC.items}
                                columns={columns}
                                controlColumns={[]}
                                loaded={headerC.loaded}
                                searchParams={headerC.searchParams}
                                collection={headerC}
                                onRowClick={onRowClick}
                                updateCollection={updateHeaderC}
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
                    title={
                        viewMode === 'add'
                            ? 'Add Header'
                            : viewMode === 'edit'
                                ? 'Edit Header'
                                : ''
                    }
                    details={headerDetails}
                    setDetails={setHeaderDetail}
                    // tabs={tabs}
                    // setTabs={setTabs}
                    // activeTab={activeTab}
                    // setActiveTab={setActiveTab}
                    // label='Company Details'
                    // profileImg='/company-img.svg'
                    // keyValueDataList={keyValueDataList}
                    // labelTwo='Team Details'
                    // labelValueData={labelValueData}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne='Previous Buyer'
                    buttonTextTwo='Next Buyer'
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    // totalDisputes={disputeDetails}
                    // disputesKeyValue={disputesKeyValue[0]}
                    onSearch={handleSearch}
                    // toggleTeamModal={toggleTeamModal}
                    // setTeamDetails={setTeamDetails}
                    setIndex={setHeaderIndex}
                    index={headerIndex}
                    collection={headerC}
                    // usersByCompanyId={bueyrByCompanyId}
                    // purchasesKeyValue={purchasesKeyValue[0]}
                    // totalPurchase={purchaseDetails}
                    // updateCollectionOne={updateDisputeC}
                    // updateCollectionTwo={updatePurchaseC}
                    updateData={updateHeaderData}
                    updateOnChange={onUpdateHeaderDataInputChange}
                    // handleUpdate={handleUpdate}
                    onAddDataInputChange={onAddHeaderDataInputChange}
                    addData={addHeaderData}
                    setUpdateData={setUpdateHeaderData}
                    viewDetailsBtn={true}
                    summaryView={false}
                    showDropDown={showDropDown}
                    toggleDropDown={toggleDropDown}
                    selectedDocument={selectedDocument}
                    setSelectedDocument={setSelectedDocument}
                    uploadedFile={uploadedFile}
                    setUploadedFile={setUploadedFile}
                    onChange={handleFileUpload}
                    onClick={handleAddClick}
                    fileInputRef={fileInputRef}
                    handleDragOver={handleDragOver}
                    handleDrop={handleDrop}
                    handleDropFile={handleDropFile}
                    page='header'
                />
            </div>
        }

    </div>
}