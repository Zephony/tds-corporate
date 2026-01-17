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

import { formatDateTime, getCollectionSearchParamsFromPage } from '@/helpers'
import { copy } from '@/helpers'
import useRequest from '@/hooks/useRequest'

import '@/css/pages/review.css'
import StatusText from '@/components/statusText'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import { Input } from '@/components/form'

import '@/css/pages/blog.css'

// Form initial Data
const initialUpdateBlogData = {
    status: '',
    name: '',

}

// Form initial Data
const initialAddBlogData = {
    name: '',
    status: '',
}

export default function Blog() {

    const { request } = useRequest()

    const [blogC, updateBlogC] = useCollection('admin/blogs', getCollectionSearchParamsFromPage())
    const [showDeleteModal, toggleDeleteModal] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()

    const [isEditable, setIsEditable] = useState(false)

    const [editIndex, setEditIndex] = useState()

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'Added on',
            id: 'created_at',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{formatDateTime(row.created_at)}</div>
        },
        {
            name: 'Title',
            id: 'title',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type'>{row.title}</div>
        },
        {
            name: 'Category',
            id: 'category',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='name'>
                    {row.category_details.name}
                </div>
            </div>
        },
        {
            name: 'Created By',
            id: 'created_by',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.user_details?.name}
            </div>
        },
        {
            name: 'Publication Status',
            id: 'publication_status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                className={`status-main ${row?.publication_status === 'PUBLISHED'
                    ? 'green'
                    : row?.publication_status === 'PENDING'
                        ? 'yellow'
                        : row?.publication_status === 'HIDDEN'
                            ? 'grey'
                            : row?.publication_status === 'FLAGGED'
                                ? 'red'
                                : ''
                    }`}
            >
                {row?.publication_status}
            </div>
        },
        {
            name: 'Blog Status',
            id: 'blog_status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                className={`status-main ${row?.blog_status === 'ACTIVE'
                    ? 'green'
                    : row?.blog_status === 'PENDING'
                        ? 'yellow'
                        : row?.blog_status === 'HIDDEN' || row?.blog_status === 'ARCHIVED'
                            ? 'grey'
                            : row?.blog_status === 'FLAGGED'
                                ? 'red'
                                : ''
                    }`}
            >
                {row?.blog_status}
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
                            setReviewDetails(row)
                            setUpdateBlogData({
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
                            setDeleteModalDescription('Are you sure, want to delete this Review')
                            setDeleteModalTitle('Delete Review')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setReviewId(row.id)
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

    const [categoryC, updateCategoryC] = useCollection('admin/blogs', getCollectionSearchParamsFromPage() )

    const [categoryColumn, setCategoryColumn] = useState([
        {
            name: 'Title',
            id: 'title',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index, isEditing) => <>
             { isEditing
                ? <div className="edit-section">
                    {console.log('Inside blog render - updateBlogDataRef.current:', updateBlogDataRef.current)}
                    <Input
                        label=''
                        name='name'
                        value={updateBlogDataRef.current['name'] || ''}
                        onChange={onUpdateBlogDataInputChange}
                        className='table-edit'
                    />
                </div>
                : <div className='panel-review-date'>
                    {row.category_details.name}
                </div>
             }
            </>
            
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                className={`status-main ${row?.category_details.status === 'ACTIVE'
                    ? 'green'
                    : row?.category_details.status === 'PENDING'
                        ? 'yellow'
                        : row?.category_details.status === 'HIDDEN' || row?.category_details.status === 'ARCHIVED'
                            ? 'grey'
                            : row?.category_details.status === 'FLAGGED'
                                ? 'red'
                                : ''
                    }`}
            >
                {row?.category_details.status}
            </div>
        },
        {
            name: '',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index, isEditing) => <div className='action'>
                {isEditing
                    ? <div className='edit-action'>
                        <div onClick={() => setEditIndex(null)} className='save'>
                            <img src='/green-check.svg' />
                        </div>
                        <div onClick={() => setEditIndex(null)} className='cancel'>
                            <img src='/edit-cancel.svg' />
                        </div>
                    </div>
                    : <div className='action-button'>
                        <button
                            onClick={(e) => {
                                e.stopPropagation()

                                setEditIndex(row.id)
                                // setViewMode('edit')
                                // setReviewDetail(row)
                                setUpdateBlogData(prev => ({
                                    ...prev,
                                    name: row.category_details.name,
                                }))
                            }}
                            className='panel-edit-icon-wrapper'
                        >
                            <img
                                className='edit-icon'
                                src='/edit-icon.svg'
                            />
                        </button>
                        <button
                            onClick={(e) => {
                                e.stopPropagation()
                                setDeleteModalDescription('Are you sure, want to delete this Review')
                                setDeleteModalTitle('Delete Review')
                                setDeleteBtn('Delete')
                                toggleDeleteModal()
                                setReviewId(row.id)
                            }}
                            className='panel-delete-icon-wrapper'
                        >
                            <img
                                className='delete-icon'
                                src='/delete-icon.svg'
                            />
                        </button>
                    </div>
                }
            </div>
        },

    ])

    const [queryParams, setQueryParam] = useQueryParams()

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showWordsModal, toggleWordsModal] = useToggle()


    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [blogIndex, setBlogIndex] = useState()

    // Store the clicked buyer from table row click
    const [blogDetails, setBlogDetails] = useState()

    const [
        addBlogData,
        setAddBlogData,
        onAddBlogDataInputChange,
        addBlogDataErrors,
        setAddBlogDataErrorsMap,
        addBlogDataErrorMessage,
        setAddBlogDataErrorMessage,
    ] = useForm(copy(initialAddBlogData))


    // Create the form for editng the buyer Data
    const [
        updateBlogData,
        setUpdateBlogData,
        onUpdateBlogDataInputChange,
        updateBlogDataErrors,
        setUpdateBlogDataErrorsMap,
        updateBlogDataErrorMessage,
        setUpdateBlogDataErrorMessage,
    ] = useForm(copy(initialUpdateBlogData))

    // Use ref to store current state for render functions
    const updateBlogDataRef = useRef(updateBlogData)
    updateBlogDataRef.current = updateBlogData

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    const [message, setMessage] = useState([])

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addBlogData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateBlogC({ reload: true })
            setAddBlogData(copy(initialAddBlogData))
            showMessagee('success', 'Blog updated successfully!')
        } catch (err) {
            // console.error('Failed to add user:', err)
            // alert('Failed to add user')
            showMessagee('error', 'Failed to update Blog')
        }
    }

    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateBlogC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }
    const handleCategorySearch = qString => {
        setQueryParam('q', qString)

        updateCategoryC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateBlogData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        try {
            await request.patch(`blog/${blogC.items[blogIndex].id}`, requestData)
            updateBlogC({ reload: true })
            showMessagee('success', 'Review updated successfully!')
            setUpdateBlogData(copy(initialUpdateBlogData))
        } catch (err) {
            console.error('Failed to update user:', err)
            showMessagee('error', 'Failed to update Review')
        }
    }

    const addCategory = async () => {
        let requestData = copy(updateBlogData)

        try {
            await request.post(`blog/${blogC.items[blogIndex].id}`, requestData)
            updateBlogC({ reload: true })
            setUpdateBlogData(copy(initialUpdateBlogData))
            showMessagee('success', 'Category added successfully!')
        }
        catch (err) {
            console.error('Failed to update user:', err)
            showMessagee('error', 'Failed to add Category')
        }
    }

    // Store buyers by company ID
    const [reviewId, setReviewId] = useState()

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`reviewa/${id}`)
            updateBlogC({ reload: true })
            showMessagee('success', 'Buyer Deleted Successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to delete buyer')
        }
    }

    // On table row click get the row index 
    // and return that particular item
    // const onRowClick = (e, index) => {
    //     e.stopPropagation()
    //     toggleRightSidePanel()
    //     setBlogIndex(index)
    //     setBlogDetails(blogC.items[index])
    //     setViewMode('view')
    // }


    function handleNextButton() {
        const newIndex = blogIndex + 1
        setBlogIndex(newIndex)
        setBlogDetails(blogC?.items[newIndex])

    }

    function handlePrevButton() {
        const newIndex = blogIndex - 1
        setBlogIndex(newIndex)
        setBlogDetails(blogC?.items[newIndex])
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
                    title='Blogs'
                />
                <div className='main-content-body'>
                    <div className='table-wrapper'>
                        <TablePageHeader
                            title='Blogs List'
                            onSearch={handleSearch}
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            // moreOptionVisible
                            showActionButtons
                            // blogButtonVisible
                            buttonText='View Categories'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                            updateCollection={updateBlogC}
                            showMoreOption={showMoreOption}
                            toggleMoreOption={toggleMoreOption}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={blogC.items}
                                columns={columns}
                                controlColumns={[]}
                                loaded={blogC.loaded}
                                searchParams={blogC.searchParams}
                                collection={blogC}
                                // onRowClick={onRowClick}
                                updateCollection={updateBlogC}
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
                    setBlogIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={viewMode === 'view'
                        ? 'Review Information'
                        : viewMode === 'edit'
                            ? 'Edit Review'
                            : viewMode === 'add'
                                ? 'Category List'
                                : ''
                    }
                    details={blogDetails}
                    setDetails={setBlogDetails}
                    offensiveWordsColumn={categoryColumn}
                    setOffensiveWordsColumn={setCategoryColumn}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Review'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Review'
                            : viewMode === 'edit' || viewMode === 'add'
                                ? 'Save'
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
                        : viewMode === 'edit'
                            ? handleUpdate
                            : viewMode === 'add'
                                ? handleAdd
                                : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    onSearch={handleCategorySearch}
                    setIndex={setBlogIndex}
                    index={blogIndex}
                    collection={blogC}
                    updateCollectionOne={updateBlogC}
                    updateData={
                        viewMode === 'edit'
                            ? updateBlogData
                            : viewMode === 'add'
                                ? addBlogData
                                : ''
                    }
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateBlogDataInputChange
                            : viewMode === 'add'
                                ? onAddBlogDataInputChange
                                : ''
                    }
                    onAddDataInputChange={onAddBlogDataInputChange}
                    addData={addBlogData}
                    setUpdateData={viewMode === 'edit'
                        ? setUpdateBlogData
                        : viewMode === 'add'
                            ? setAddBlogData
                            : ''
                    }
                    viewDetailsBtn={true}
                    summaryView={false}
                    showDropDown={showDropDown}
                    toggleDropDown={toggleDropDown}
                    toggleWordsModal={toggleWordsModal}
                    showWordsModal={showWordsModal}
                    page='blog'
                    addOffensiveWord={addCategory}
                    updateCollectionTwo={updateCategoryC}
                    collectionTwo={categoryC}
                    isEditable={isEditable}
                    setIsEditable={setIsEditable}
                    editIndex={editIndex}
                    setEditIndex={setEditIndex}
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
                    buyerByCompanyId={reviewId}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }
    </div>
}