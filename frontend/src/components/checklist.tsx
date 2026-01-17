'use client'

import { useState } from 'react'
import DropList from './dropList'
import TagInput from './tagInput'

interface ChecklistProps {
    title: string
    subtitle: string
    text: string
    subtitleText: string
    items: any[]
    showKeywordsModal?: any
    toggleKeywordsModal?: any
    handleAddKeyword?: any
}

export default function Checklist(props: ChecklistProps) {
    const [activeItemIndex, setActiveItemIndex] = useState(null)

    const handleAddKeywordsClick = (index) => {
        setActiveItemIndex(index)
        props.toggleKeywordsModal()
    }

    return <div className='checklist-container'>
        <div className='header'>
            <div className='header-left'>
                <div className='header-left-title'>{props.title}</div>
                <div className='header-left-subtitle'>Uploaded Date</div> 
            </div>
            <div className='header-right'>
                <button className='link-like-button'>{props.text}</button>
                <div className='header-right-subtitle'> Feb 20, 2025</div>
            </div>
        </div>
        <hr className='hr-line' />
        <div className='content'>
            {props.items.map((item, index) => (
                <div className='content-item' key={index}>
                    <div className='content-left'>
                        <img className='content-left-img' src={item.keyWord.length > 0 ? '/green-check.svg' : '/cross.svg'} alt={item.keyWord.length > 0 ? 'check' : 'cross'} />
                        <div className='content-left-title'>{item.label}</div>
                    </div>
                    <div className='content-right'>
                        {item.keyWord.length > 0 
                            ? <div className='content-right-text'>
                                {item.keyWord.length} keywords matched
                            </div> 
                            : <div className='content-right-text'> 
                                <div className='not-found-text'>
                                    No keywords found
                                </div> 
                                <div style={{ position: 'relative' }}>
                                    <button 
                                        className='link-like-button'
                                        onClick={() => handleAddKeywordsClick(index)}
                                    >
                                        Add Keywords
                                    </button>
                                    {props.showKeywordsModal && activeItemIndex === index && (
                                        <DropList
                                            title='Add New Keywords'
                                            name='tag-input-drop-list'
                                        >
                                            <TagInput
                                                label='Keywords'
                                                toggleWordsModal={props.toggleKeywordsModal}
                                                addOffensiveWord={props.handleAddKeyword}
                                            />
                                        </DropList>
                                    )}
                                </div>
                            </div>
                        }
                    </div>
                </div>
            ))}

        </div>
    </div>
}