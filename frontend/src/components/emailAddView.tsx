'use client'

import { useState, useEffect, useRef } from 'react'
import { Input, SelectField } from './form'

interface EmailAddViewProps {
    updateData?: any
    updateOnChange?: any
    viewMode?: 'add' | 'edit'
}

// Client tags list
const clientTags = [
    { name: '$title', value: '$title' },
    { name: '$first_name', value: '$first_name' },
    { name: '$last_name', value: '$last_name' },
    { name: '$surname', value: '$surname' },
    { name: '$company_name', value: '$company_name' },
    { name: '$buyer_id', value: '$buyer_id' },
    { name: '$seller_id', value: '$seller_id' },
    { name: '$email', value: '$email' },
    { name: '$primary_email', value: '$primary_email' },
]

// Company tags list
const companyTags = [
    { name: '$platform_name', value: '$platform_name' },
    { name: '$help_centre_link', value: '$help_centre_link' },
    { name: '$company_address', value: '$company_address' },
    { name: '$company_phone', value: '$company_phone' },
    { name: '$support_email', value: '$support_email' },
]

export default function EmailAddView(props: EmailAddViewProps) {
    const [showClientTags, setShowClientTags] = useState<{ [key: string]: boolean }>({})
    const [showCompanyTags, setShowCompanyTags] = useState<{ [key: string]: boolean }>({})
    const dropdownRefs = useRef<{ [key: string]: HTMLDivElement | null }>({})

    // Close dropdowns when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            Object.keys(dropdownRefs.current).forEach(fieldName => {
                const ref = dropdownRefs.current[fieldName]
                if (ref && !ref.contains(event.target as Node)) {
                    setShowClientTags(prev => ({ ...prev, [fieldName]: false }))
                    setShowCompanyTags(prev => ({ ...prev, [fieldName]: false }))
                }
            })
        }

        document.addEventListener('mousedown', handleClickOutside)
        return () => {
            document.removeEventListener('mousedown', handleClickOutside)
        }
    }, [])

    const toggleClientTags = (fieldName: string) => {
        setShowClientTags(prev => ({
            ...prev,
            [fieldName]: !prev[fieldName]
        }))
        // Close company tags when opening client tags
        setShowCompanyTags(prev => ({
            ...prev,
            [fieldName]: false
        }))
    }

    const toggleCompanyTags = (fieldName: string) => {
        setShowCompanyTags(prev => ({
            ...prev,
            [fieldName]: !prev[fieldName]
        }))
        // Close client tags when opening company tags
        setShowClientTags(prev => ({
            ...prev,
            [fieldName]: false
        }))
    }

    const handleTagSelect = (fieldName: string, tagValue: string, tagType: 'client' | 'company') => {
        const currentValue = props?.updateData?.[fieldName] || ''
        const newValue = currentValue ? `${currentValue} ${tagValue}` : tagValue
        
        if (props.updateOnChange) {
            const syntheticEvent = {
                target: {
                    name: fieldName,
                    value: newValue
                }
            }
            props.updateOnChange(syntheticEvent)
        }

        // Close the dropdown after selection
        if (tagType === 'client') {
            setShowClientTags(prev => ({ ...prev, [fieldName]: false }))
        } else {
            setShowCompanyTags(prev => ({ ...prev, [fieldName]: false }))
        }
    }

    const renderTagLinks = (fieldName: string) => {
        return (
            <div 
                className='tag-links-wrapper'
                ref={(el) => {
                    dropdownRefs.current[fieldName] = el
                }}
            >
                <button
                    type='button'
                    className='link-like-button'
                    onClick={(e) => {
                        e.stopPropagation()
                        toggleClientTags(fieldName)
                    }}
                >
                    Add Client tags
                </button>
                <button
                    type='button'
                    className='link-like-button'
                    onClick={(e) => {
                        e.stopPropagation()
                        toggleCompanyTags(fieldName)
                    }}
                >
                    Add Company tags
                </button>
                
                {/* Client Tags Dropdown */}
                {showClientTags[fieldName] && (
                    <div className='tags-dropdown'>
                        <div className='tags-dropdown-title'>Client Tags</div>
                        <div className='tags-dropdown-list'>
                            {clientTags.map((tag, index) => (
                                <button
                                    key={index}
                                    type='button'
                                    className='tag-item'
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        handleTagSelect(fieldName, tag.value, 'client')
                                    }}
                                >
                                    {tag.name}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Company Tags Dropdown */}
                {showCompanyTags[fieldName] && (
                    <div className='tags-dropdown'>
                        <div className='tags-dropdown-title'>Company Tags</div>
                        <div className='tags-dropdown-list'>
                            {companyTags.map((tag, index) => (
                                <button
                                    key={index}
                                    type='button'
                                    className='tag-item'
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        handleTagSelect(fieldName, tag.value, 'company')
                                    }}
                                >
                                    {tag.name}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        )
    }

    return (
        <div className='edit-wrapper email-add-view'>
            {/* Template Name */}
            <div className='edit-section'>
                <Input
                    label='Template Name'
                    name='template_name'
                    value={props?.updateData?.['template_name'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: Welcome Email'
                />
            </div>

            {/* Active and Agent Active Dropdowns */}
            <div className='edit-section dropdown-row'>
                <SelectField
                    label='Active'
                    name='active'
                    placeholder='Select'
                    options={[
                        { name: 'Yes', value: 'yes' },
                        { name: 'No', value: 'no' }
                    ]}
                    value={props?.updateData?.['active'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    viewMode='edit'
                />
                <SelectField
                    label='Agent Active'
                    name='agent_active'
                    placeholder='Select'
                    options={[
                        { name: 'Yes', value: 'yes' },
                        { name: 'No', value: 'no' }
                    ]}
                    value={props?.updateData?.['agent_active'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    viewMode='edit'
                />
            </div>

            {/* Attachment and Client View Dropdowns */}
            <div className='edit-section dropdown-row'>
                <SelectField
                    label='Attachment'
                    name='attachment'
                    placeholder='Select'
                    options={[
                        { name: 'Yes', value: 'yes' },
                        { name: 'No', value: 'no' }
                    ]}
                    value={props?.updateData?.['attachment'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    viewMode='edit'
                />
                <SelectField
                    label='Client View'
                    name='client_view'
                    placeholder='Select'
                    options={[
                        { name: 'Yes', value: 'yes' },
                        { name: 'No', value: 'no' }
                    ]}
                    value={props?.updateData?.['client_view'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    viewMode='edit'
                />
            </div>

            {/* To Field */}
            <div className='edit-section-email'>
                <Input
                    label='To'
                    name='to'
                    value={props?.updateData?.['to'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: name@xyzmail.com'
                />
                {renderTagLinks('to')}
            </div>

            {/* CC Field */}
            <div className='edit-section-email'>
                <Input
                    label='CC'
                    name='cc'
                    value={props?.updateData?.['cc'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: name@xyzmail.com'
                />
                {renderTagLinks('cc')}
            </div>

            {/* BCC Field */}
            <div className='edit-section-email'>
                <Input
                    label='BCC'
                    name='bcc'
                    value={props?.updateData?.['bcc'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: name@xyzmail.com'
                />
                {renderTagLinks('bcc')}
            </div>

            {/* Subject Field */}
            <div className='edit-section-email'>
                <Input
                    label='Subject'
                    name='subject'
                    value={props?.updateData?.['subject'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: Welcome to the $platform_name'
                />
                {renderTagLinks('subject')}
            </div>

            {/* Message Field */}
            <div className='edit-section-email'>
                <Input
                    label='Message'
                    name='message'
                    value={props?.updateData?.['message'] || props?.updateData?.['body'] || ''}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    type='textarea'
                    placeholder='Email message'
                />
                {renderTagLinks('message')}
            </div>
        </div>
    )
}

