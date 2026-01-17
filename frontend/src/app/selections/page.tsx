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
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

// Form initial Data
const initialUpdateSelectionData = {
    data_type: '',
    category_name: '',
    sub_category_name: '',
    img: '',
    status: '',
    selection_name:''
}

// Form initial Data
const initialAddSelectionData = {
    data_type: '',
    category_name: '',
    sub_category_name: '',
    img: '',
    status: '',
    selection_name: ''
}

export default function Selections() {

    const { request } = useRequest()

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'S.No',
            id: 'id',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{row.id}</div>
        },
        {
            name: 'Data Type',
            id: 'data_type',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type'>{row.data_type_details.name}</div>
        },
        {
            name: 'Category Name',
            id: 'category_name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='category-img'>
                    <img src='/demo-icon.svg'></img>
                </div>
                <div className='name'>
                    {row.category_details.name}
                </div>
            </div>
        },
        {
            name: 'Sub Category Name',
            id: 'sub_category_name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='category-img'>
                    <img src='/demo-icon.svg'></img>
                </div>
                <div className='name'>
                    {row.sub_category_details.name}
                </div>
            </div>
        },
        {
            name: 'Selections',
            id: 'name',
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
            name: 'Sub Category ID',
            id: 'id_sub_category',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>{row.id_sub_category}</div>
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
                            setSelectionIndex(index)
                            setSelectionDetail(selectionC.items[index])
                            setUpdateSelectionData({
                                data_type: row.data_type_details.name,
                                category_name: row.category_details.name,
                                img: '/demo-icon.svg',
                                status: row.status,
                                sub_category_name: row?.sub_category_details.name,
                                selections: row.name
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
                    <button 
                        onClick={(e) => {
                            e.stopPropagation()
                            setDeleteModalDescription('Are you sure, want to delete this Sub Category')
                            setDeleteModalTitle('Delete Sub Category')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setSubCategoryById(row.id)
                        }}
                        className='delete-icon-wrapper'
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

    const [queryParams, setQueryParam] = useQueryParams()
    const [selectionC, updateSelectionC] = useCollection('admin/selections', getCollectionSearchParamsFromPage())

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showDeleteModal,  toggleDeleteModal] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()


    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [selectionIndex, setSelectionIndex] = useState()

    const [selectedDocument, setSelectedDocument] = useState([])
    const [uploadedFile, setUploadedFile] = useState()

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    const [message, setMessage] = useState([])


    // Store buyers by company ID
    const [subCategoryById, setSubCategoryById] = useState()

    const [
        addSelectionData,
        setAddSelectionData,
        onAddSelectionDataInputChange,
        addSelectionDataErrors,
        setAddSelectionDataErrorsMap,
        addSelectionDataErrorMessage,
        setAddSelectionDataErrorMessage,
    ] = useForm(copy(initialAddSelectionData))


    // Create the form for editng the buyer Data
    const [
        updateSelectionData,
        setUpdateSelectionData,
        onUpdateSelectionDataInputChange,
        updateSelectionDataErrors,
        setUpdateSelectionDataErrorsMap,
        updateSelectionDataErrorMessage,
        setUpdateSelectionDataErrorMessage,
    ] = useForm(copy(initialUpdateSelectionData))

    // Store the clicked buyer from table row click
    const [selectionDetails, setSelectionDetail] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    const fileInputRef = useRef()
    console.log(queryParams, 'q and queryparams')


    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateSelectionC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
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

        setSelectionIndex(index)
        setSelectionDetail(selectionC.items[index])
        setViewMode('view')
    }

    // Display the request status
    const showMessagee = (status: string, text: string) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateSelectionData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        try {
            await request.patch(`selections/${selectionC.items[clickedBuyerIndex].id}`, requestData)
            updateSelectionC({ reload: true })
            showMessagee('success', 'Selection updated successfully!')
            setUpdateSelectionData(copy(initialUpdateSelectionData))
        } catch (err) {
            console.error('Failed to update user:', err)
            // alert('Failed to update user')
            showMessagee('error', 'Failed to update Selection')
        }
    }

    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addSelectionData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateSelectionC({ reload: true })
            setAddSelectionData(copy(initialAddSelectionData))
            showMessagee('success', 'Successfully added new Selection.')
        } catch (err) {
            // console.error('Failed to add user:', err)
            // alert('Failed to add user')
            showMessagee('error', 'Failed to add Selection.')
        }
    }

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`selection/${id}`)
            updateSelectionC({ reload: true })
            showMessagee('success', 'Selection Deleted Successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to delete Selections')
        }
    }
    return <div className='page-container'>
        <StatusText
            text={message}
        />
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
                            title='Selections'
                            onSearch={handleSearch}
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            // moreOptionVisible
                            buttonText='Add'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                            setAddData={setAddSelectionData}
                            showMoreOption={showMoreOption}
                            toggleMoreOption={toggleMoreOption}
                            showActionButtons
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={selectionC.items}
                                columns={columns}
                                controlColumns={[]}
                                loaded={selectionC.loaded}
                                searchParams={selectionC.searchParams}
                                collection={selectionC}
                                onRowClick={onRowClick}
                                selectedIndex={selectionIndex}
                                updateCollection={updateSelectionC}
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
                    setSelectionIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={
                        viewMode === 'add'
                            ? 'Add Selection'
                            : viewMode === 'edit'
                                ? 'Edit Selection'
                                : ''
                    }
                    details={selectionDetails}
                    setDetails={setSelectionDetail}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Catgeory'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Category'
                            : viewMode === 'edit' || viewMode === 'add'
                                ? 'Save'
                                : ''
                    }
                    buttonOneFunction={viewMode === 'edit' || viewMode === 'add'
                        ? toggleRightSidePanel
                        : ''
                    }
                    buttonTwoFunction={viewMode === 'edit'
                        ? handleUpdate
                        : viewMode === 'add'
                            ? handleAdd
                            : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    onSearch={handleSearch}
                    setIndex={setSelectionIndex}
                    index={selectionIndex}
                    collection={selectionC}
                    updateData={
                        viewMode === 'edit'
                            ? updateSelectionData
                            : viewMode === 'add'
                                ? addSelectionData
                                : ''
                    }
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateSelectionDataInputChange
                            : viewMode === 'add'
                                ? onAddSelectionDataInputChange
                                : ''
                    }
                    onAddDataInputChange={onAddSelectionDataInputChange}
                    addData={addSelectionData}
                    setUpdateData={viewMode === 'edt'
                        ? setUpdateSelectionData
                        : viewMode === 'add'
                            ? setAddSelectionData
                            : ''
                    }
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
                    page='selection'
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
                    buyerByCompanyId={subCategoryById}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }

    </div>
}