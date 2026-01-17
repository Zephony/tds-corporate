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
import StatusText from '@/components/statusText'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'

// Form initial Data
const initialUpdateCategoryData = {
    data_type: '',
    category_name: '',
    img: '',
    status: '',
}

// Form initial Data
const initialAddCategoryData = {
    data_type: '',
    category_name: '',
    img: '',
    status: '',
}

export default function Categorization() {

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
            id: 'data-type',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type'>{row.data_type_details.name}</div>
        },
        {
            name: 'Category Name',
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
            name: 'Category ID',
            id: 'id_data_type',
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
                            setCategoryIndex(index)
                            setCategoryDetail(categoriesC.items[index])
                            setUpdateCategoryData({
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
                    <button 
                        onClick={(e) => {
                            e.stopPropagation()
                            setDeleteModalDescription('Are you sure, want to delete this Category')
                            setDeleteModalTitle('Delete Category')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setBuyerByCompanyId(row.id)
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
    const [categoriesC, updateCategoriesC] = useCollection('admin/categories', getCollectionSearchParamsFromPage())

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showDeleteModal,  toggleDeleteModal] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()


    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [categoryIndex, setCategoryIndex] = useState()

    const [selectedDocument, setSelectedDocument] = useState([])
    const [uploadedFile, setUploadedFile] = useState()

    const [
        addCategoryData,
        setAddCategoryData,
        onAddCategoryDataInputChange,
        addCategoryDataErrors,
        setAddCategoryDataErrorsMap,
        addBCategoryDataErrorMessage,
        setAddCategoryDataErrorMessage,
    ] = useForm(copy(initialAddCategoryData))


    // Create the form for editng the buyer Data
    const [
        updateCategoryData,
        setUpdateCategoryData,
        onUpdateCategoryDataInputChange,
        updateCategoryDataErrors,
        setUpdateCategoryDataErrorsMap,
        updateCategoryDataErrorMessage,
        setUpdateCategoryDataErrorMessage,
    ] = useForm(copy(initialUpdateCategoryData))

    // Store the clicked buyer from table row click
    const [categoryDetails, setCategoryDetail] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    const fileInputRef = useRef()
    console.log(queryParams, 'q and queryparams')

    const [message, setMessage] = useState([])

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    // Store buyers by company ID
    const [categoryById, setCategoryById] = useState()

    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateCategoriesC(old => {
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

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`category/${id}`)
            updateCategoriesC({ reload: true })
            showMessagee('success', 'Category Deleted Successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to delete Category')
        }
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

        setCategoryIndex(index)
        setCategoryDetail(categoriesC.items[index])
        setViewMode('view')
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateCategoryData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        try {
            await request.patch(`categories/${categoriesC.items[clickedBuyerIndex].id}`, requestData)
            updateCategoriesC({ reload: true })
            showMessagee('success', 'Categories updated successfully!')
            setUpdateCategoryData(copy(initialUpdateCategoryData))
        } catch (err) {
            console.error('Failed to update user:', err)
            // alert('Failed to update user')
            showMessagee('error', 'Failed to update Categories' )
        }
    }

    // Add functionality
    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addCategoryData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateCategoriesC({ reload: true })
            setAddCategoryData(copy(initialAddCategoryData))
            showMessagee('success', 'Successfully added new category.')
        } catch (err) {
            showMessagee('error', 'Failed to add category.')
        }
    }

    // Display the request status
    const showMessagee = (status: string, text: string) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
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
                            title='Category'
                            onSearch={handleSearch}
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            // moreOptionVisible
                            buttonText='Add Category'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                            setAddData={setAddCategoryData}
                            showMoreOption={showMoreOption}
                            toggleMoreOption={toggleMoreOption}
                            showActionButtons
                        />
                        <div className='table-container'>                
                            <Table
                                className='category-table'
                                items={categoriesC.items}
                                columns={columns}
                                controlColumns={[]}
                                loaded={categoriesC.loaded}
                                searchParams={categoriesC.searchParams}
                                collection={categoriesC}
                                onRowClick={onRowClick}
                                updateCollection={updateCategoriesC}
                                selectedIndex={categoryIndex}
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
                            ? 'Add Category' 
                            : viewMode === 'edit' 
                                ? 'Edit Category' 
                                : ''
                    }
                    details={categoryDetails}
                    setDetails={setCategoryDetail}
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
                    buttonOneFunction={ viewMode === 'edit' || viewMode === 'add'
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
                    setIndex={setCategoryIndex}
                    index={categoryIndex}
                    collection={categoriesC}
                    updateData={
                        viewMode === 'edit'
                            ? updateCategoryData
                            : viewMode === 'add'
                                ? addCategoryData
                                : ''
                    }
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateCategoryDataInputChange
                            : viewMode === 'add'
                                ? onAddCategoryDataInputChange
                                : ''
                    }
                    onAddDataInputChange={onAddCategoryDataInputChange}
                    addData={addCategoryData}
                    setUpdateData={viewMode === 'edt'
                        ? setUpdateCategoryData
                        : viewMode === 'add'
                            ? setAddCategoryData
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
                    page='category'
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
                    buyerByCompanyId={categoryById}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }
        
    </div>
}