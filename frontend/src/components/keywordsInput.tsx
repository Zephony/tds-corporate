'use client'

import { useState, useEffect } from 'react'

interface KeywordsInputProps {
    label?: string
    keywords?: string[]
    onChange?: (e: any) => void
    className?: string
    name?: string
}

export default function KeywordsInput(props: KeywordsInputProps) {
    const [keywords, setKeywords] = useState<string[]>(props.keywords || [])
    const [inputValue, setInputValue] = useState('')

    // Update keywords when props change
    useEffect(() => {
        if (props.keywords) {
            setKeywords(Array.isArray(props.keywords) ? props.keywords : [])
        }
    }, [props.keywords])

    const handleKeyDown = (e) => {
        if ((e.key === 'Enter' || e.key === ',') && inputValue.trim()) {
            e.preventDefault()
            const newKeywords = [...keywords, inputValue.trim()]
            setKeywords(newKeywords)
            setInputValue('')
            
            // Trigger onChange to update form data
            if (props.onChange) {
                const event = {
                    target: {
                        name: props.name || 'keywords',
                        value: newKeywords
                    }
                }
                props.onChange(event)
            }
        }
    }

    const removeKeyword = (index) => {
        const newKeywords = keywords.filter((_, i) => i !== index)
        setKeywords(newKeywords)
        
        // Trigger onChange to update form data
        if (props.onChange) {
            const event = {
                target: {
                    name: props.name || 'keywords',
                    value: newKeywords
                }
            }
            props.onChange(event)
        }
    }

    return (
        <div className={`keywords-input-wrapper ${props.className || ''}`}>
            <div className='input-label'>{props.label || 'Keywords'}</div>
            <div className='keywords-input-container'>
                <div className='keywords-tags-input-wrapper'>
                    {keywords.map((keyword, index) => (
                        <div key={index} className='keyword-tag-input'>
                            <span>{keyword}</span>
                            <button
                                type='button'
                                onClick={() => removeKeyword(index)}
                                className='keyword-remove-btn'
                            >
                                <img
                                    src='/close-icon-dark.svg'
                                    alt='Remove'
                                    className='keyword-remove-icon'
                                />
                            </button>
                        </div>
                    ))}
                    <input
                        className='keywords-input'
                        type='text'
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                </div>
            </div>
        </div>
    )
}

