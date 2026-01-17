'use client'

import { useRef, useEffect } from 'react'

interface DropListProps {
    title?: any
    children?: any
    showDropList?: boolean
    toggleDropList?: any
    name?: any
}

export default function DropList(props: DropListProps) {
    const dropListRef = useRef()

    useEffect(() => {
        const dropList = dropListRef.current

        if(dropList) {
            // dialog.showModal()

            const handleEscapeKey = (e) => {
                if(e.key === 'Escape') {
                    props.toggleDropList()
                }
            }

            const handleClickOutside = (e) => {
                // ignore clicks on the select-field and its option list (covers portals)
                if (e.target.closest && (
                    e.target.closest('.select-field') ||
                    e.target.closest('.select-options') ||
                    e.target.closest('.select-option')
                )) {
                    return;
                }
                
                if(dropList && !dropList.contains(e.target)) {
                    props.toggleDropList()
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
    }, [])

    return <div 
        ref={dropListRef}
        className={`drop-list-wrapper ${props.name}`}
        onClick={(e) => e.stopPropagation()}
    >
        <div className='drop-list-header'>
            {props.title}
        </div>
        <hr className='drop-list-line'></hr>
        <div className='drop-list-children'>
            {props.children}
        </div>
    </div>
}

