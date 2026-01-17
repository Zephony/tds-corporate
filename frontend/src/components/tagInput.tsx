'use client'

import { useState } from 'react'

interface TagInputProps {
    label?: any
    toggleWordsModal?: any
    addOffensiveWord?: any
}

export default function TagInput(props: TagInputProps) {
    const [tags, setTags] = useState([])
    const [inputValue, setInputValue] = useState()

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && inputValue.trim()) {
            e.preventDefault()
            setTags([...tags, inputValue.trim()])
            setInputValue('')
        }
    }

    const removeTag = (index) => {
        const newTag = tags.filter((item, i) => i !== index)
        setTags(newTag)

    }

    return <div className='tag-input-wrapper' onClick={(e) => e.stopPropagation()}>
        <div className='label'>{props.label}</div>
        <div className='tag-input-container'>
            {tags.map((tag, index) => <div key={index} className='tag-wrapper'>
                <div className='tag'>
                    {tag}
                </div>
                <button onClick={(e) => {
                    e.stopPropagation();
                    removeTag(index);
                }} className='close-btn'>
                    <img
                        className='close-img'
                        src='/close-icon-dark.svg'
                    />
                </button>            
            </div>)}
            <input
            className='tag-input'
            type='text'
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            onClick={(e) => e.stopPropagation()}
            />
        </div>
        <div className='action-button-wrapper'>
            <button 
                onClick={(e) => {
                    e.stopPropagation();
                    props.toggleWordsModal?.();
                }}
                className='without-bg-btn'
            >
                Cancel
            </button>
            <button 
                onClick={(e) => {
                    e.stopPropagation();
                    if (tags.length > 0) {
                        props.addOffensiveWord?.(tags);
                    }
                }}
                className={`with-bg-btn ${tags.length === 0 ? 'disable' : ''}`}
                disabled={tags.length === 0}
            >
                Add
            </button>
        </div>
    </div>
}