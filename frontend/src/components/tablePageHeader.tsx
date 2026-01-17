'use client'

import { useContext, useEffect, useRef } from 'react'
import DropList from './dropList'
import FilterDropList from './filterDropList'

// import menu from '../assets/menu.svg'
// import { SidebarContext } from '../contexts'

interface TablePageHeaderProps {
    title?: string,
    onSearch?: any,
    q?: any,
    toggleFilterDropList?: any,
    showFilterDropList?: any
    onAddClick?: any
    onExportClick?: any
    moreOptionVisible?: any
    quickFilter?: any
    collection?: any
    onFilterInputChange?:any
    currentFilterData?: any
    applyFilter?: any
    updateCollection?: any
    sliderFilter?: any
    buttonText?: any
    toggleRightSidePanel?: any
    setViewMode?: any
    setAddData?: any
    updateData?: any
    showMoreOption?: any
    toggleMoreOption?: any
    showActionButtons?: any
    blogButtonVisible?: any
    templateButtonVisible?: any
    multipleButtons?: Array<{
        text: string,
        onClick: () => void
    }>
}

export default function TablePageHeader(props: TablePageHeaderProps) {
    const moreOptionRef = useRef()

    useEffect(() => {
        const moreOption = moreOptionRef.current

        if (moreOption) {
            // dialog.showModal()

            const handleEscapeKey = (e) => {
                if (e.key === 'Escape') {
                    props.toggleMoreOption()
                }
            }

            const handleClickOutside = (e) => {

                if (moreOption && !moreOption.contains(e.target)) {
                    props.toggleMoreOption()
                }
            }

            document.addEventListener('keydown', handleEscapeKey)
            document.addEventListener('click', handleClickOutside)

            return () => {
                document.removeEventListener('keydown', handleEscapeKey)
                document.removeEventListener('click', handleClickOutside)
                // dialog.close()
            }
        }
    }, [props.showMoreOption])
    return <div className='table-page-header'>
        <div className='table-page-header-left'>
            <div className='title'>{props.title}</div>
        </div>

        <div className='table-page-header-right'>
            {props.onSearch && <input
                id='search-input'
                type='text'
                className='search-input'
                placeholder='Search'
                onChange={e => props.onSearch(e.target.value, props.updateCollection)}
            />}

            {props.showActionButtons && <>
                {props.toggleFilterDropList && <div className='filter-btn-droplist-wrapper'>
                    <button type='button'
                        id='open-filters-form-button'
                        className='filters web'
                        onClick={props.toggleFilterDropList}
                    >
                        Filters
                    </button>
                    {props.showFilterDropList &&
                        <FilterDropList
                            quickFilter={props.quickFilter}
                            toggleFilterDropList={props.toggleFilterDropList}
                            showFilterDropList={props.showFilterDropList}
                            isDateDropList={false}
                            isDateInput={true}
                            collection={props.collection}
                            currentFilterData={props.currentFilterData}
                            sliderFilter={props.sliderFilter}
                            updateCollection={props.updateCollection}
                            updateData={props.updateData}
                        />
                    }
                </div>}

                {props.multipleButtons && props.multipleButtons.map((btn, index) => (
                    <button 
                        key={index}
                        type='button'
                        id={`open-add-form-button-${index}`}
                        className='add'
                        onClick={btn.onClick}
                    >
                        {btn.text}
                    </button>
                ))}

                {props.onAddClick && !props.multipleButtons && <button type='button'
                    id='open-add-form-button'
                    className='add'
                    onClick={() => {
                        props.setViewMode('add')
                        props.toggleRightSidePanel()
                        
                    }}
                >
                    {props.buttonText}
                </button>}

                {props.templateButtonVisible && (
                    <>
                        <button 
                            type='button'
                            id='open-add-form-button'
                            className='add'
                            onClick={() => {
                                props.setViewMode('add')
                                props.toggleRightSidePanel()
                            }}
                        >
                            Send Email
                        </button>
                        <button 
                            type='button'
                            id='open-add-form-button'
                            className='add'
                            onClick={() => {
                                props.setViewMode('add')
                                props.toggleRightSidePanel()
                            }}
                        >
                            Assign Template
                        </button>
                    </>
                )}

                {props.moreOptionVisible && <div className='more-button-wrapper'>
                        <button type='button'
                            id='open-more-button'
                            className='add' 
                            onClick={props.toggleMoreOption}
                        >
                            <img className='more-icon' src='/more-icon.svg'/>
                        </button>

                        {props.showMoreOption &&
                            <div ref={moreOptionRef} className='more-modal-wrapper'>
                                <button className='more-button'>
                                    View Blocked Users
                                </button>
                            </div>
                        }
                    </div>
                }
                {props.blogButtonVisible &&
                    <button id='open-add-form-button'>
                        Add Blog
                    </button>
                }
            </>}
        </div>
    </div>
}