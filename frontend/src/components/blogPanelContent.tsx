'use client'

import { Input, SelectField } from './form'

import { getOptions, replaceUnderScoreWithSpace } from '@/helpers'

import Table from './table'
import { link } from 'fs'
import DropList from './dropList'
import TagInput from './tagInput'
import useToggle from '@/hooks/useToggle'
import KeyValue from './keyValue'

interface BlogPanelContentProps {
    page?: any
    label?: any
    details?: any
    search?: any
    viewMode?: any
    collection?: any
    updateData?: any
    showWordsModal?: any
    updateOnChange?: any
    toggleWordsModal?: any
    addOffensiveWord?: any
    updateCollection?: any
    labelValueData?: any
    offensiveWordsColumn?: any
    setOffensiveWordsColumn?: any
    isEditable?: any
    setIsEditable?: any
    editIndex?: any
    setEditIndex?: any
}

export default function BlogPanelContent(props: BlogPanelContentProps) {
    console.log(props.collection.items, 'labelvaluedata')
    return <div className='review-panel-content-wrapper'>
        {props.viewMode === 'view' &&
            <div className='key-value-section'>
                {props.labelValueData.map(item =>
                    <div className='key-values-wrapper'>
                        <div className={'key-value-label'}>
                            {item.displayKey}
                        </div>
                        <div className={'key-value-value'}>
                            {item.value}
                        </div>
                    </div>
                )}
            </div>
        }
        {props.viewMode === 'edit' && <div className='review-panel-edit-view'>
            <div className='key-value-section'>
                {props.labelValueData.map(item =>
                    <KeyValue
                        displayKey={item.displayKey}
                        value={item.value}
                    />
                )}
            </div>
            <div className='edit-wrapper'>
                <div className="edit-section">
                    <SelectField
                        label='Status'
                        name='status'
                        value={props?.updateData['status']}
                        onChange={props.updateOnChange}
                        className='input-wrapper'
                        options={props.collection.loaded
                            ? getOptions([...new Set(props.collection.items.map(item => item?.status))]
                                .map(status => ({ status })), 'status', 'status')
                            : []
                        }
                    />
                </div>
            </div>
        </div>}
        {props.viewMode === 'add' && <div>
            <div className='review-panel-header'>
                {props.search && <input
                    id='search-input'
                    type='text'
                    className='search-input'
                    placeholder='Search'
                    onChange={e => props.search(e.target.value, props.updateCollection)}
                />}
                <div className='link-like-button-wrapper'>
                    <button onClick={props.toggleWordsModal} className='link-like-button'>
                        Add Category
                    </button>
                    {props.showWordsModal &&
                        <DropList
                            title='Add Category'
                            name='category-drop-list'
                        >
                            <div className='add-category-wrapper'>
                                <div className='edit-wrapper'>
                                    <div className="edit-section">
                                        <Input
                                            label='Name'
                                            name='name'
                                            placeholder='Ex. Name'
                                            value={props?.updateData['name']}
                                            onChange={props.updateOnChange}
                                            className='input-wrapper'
                                        />
                                    </div>
                                    <div className="edit-section">
                                        <SelectField
                                            label='Status'
                                            name='status'
                                            placeholder={props?.updateData['status']}
                                            value={props?.updateData['status']}
                                            onChange={props.updateOnChange} 
                                            className='input-wrapper'
                                            options={props.collection.loaded
                                                ? getOptions([...new Set(props.collection.items.map(item => replaceUnderScoreWithSpace(item?.blog_status)))]
                                                    .map(status => ({ status })), 'status', 'status')
                                                : []
                                            }
                                        />
                                    </div>
                                </div>
                                <div className='action-button-wrapper'>
                                    <button
                                        onClick={props.toggleWordsModal}
                                        className='without-bg-btn'
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={() => props.addOffensiveWord()}
                                        className={`with-bg-btn ${props.updateData.name === '' ? 'disable' : ''}`}
                                    >
                                        Add
                                    </button>
                                </div>
                            </div>
                        </DropList>
                    }
                </div>
            </div>
            <div className='offensive-words-table'>
                <Table
                    items={props.collection.items}
                    columns={props.offensiveWordsColumn}
                    controlColumns={[]}
                    loaded={props.collection.loaded}
                    searchParams={props.collection.searchParams}
                    collection={props.collection}
                    updateCollection={props.updateCollection}
                    className='offensive-words-table'
                    // onEditIconClick={props.onEditIconClick}
                    editIndex={props.editIndex}
                    setIsEditable={props.setIsEditable}
                    isEditable={props.isEditable}

                />
            </div>
        </div>}
    </div>
}