'use client'

import React, { useState, useEffect, useRef } from 'react'


export default function Modal(props) {
    const dialogRef = useRef(null)

    useEffect(() => {
        const dialog = dialogRef.current
        if (dialog) {
            // Show the dialog when component mounts
            dialog.showModal()

            // Handle escape key and clicking outside
            const handleEscape = (e) => {
                if (e.key === 'Escape') {
                    props.toggleModal()
                }
            }

            const handleClickOutside = (e) => {
                if (e.target === dialog) {
                    props.toggleModal()
                }
            }

            document.addEventListener('keydown', handleEscape)
            dialog.addEventListener('click', handleClickOutside)

            return () => {
                document.removeEventListener('keydown', handleEscape)
                dialog.removeEventListener('click', handleClickOutside)
                dialog.close()
            }
        }
    }, [])

    return (
        <dialog
            ref={dialogRef}
            className={`modal ${props.className || ''}`}
        >
            {!props.noHeader && <ModalHeader title={props.title}
                toggleModal={props.toggleModal}
            />}

            {props.children}
        </dialog>
    )
}

function ModalHeader(props) {
    return <div className='header'>
        <h2>{props.title}</h2>

        <button
            type='button'
            className='cobb close-button'
            onClick={e => {
                e.preventDefault()
                e.stopPropagation()
                props.toggleModal()
            }}
        >
            <img src='/close-icon.svg'
                className='modal-close'
                alt='Modal close icon'
            />
        </button>
    </div>
}