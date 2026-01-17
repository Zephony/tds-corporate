'use client'

import { useState, useRef, useEffect } from 'react'

interface UploadProps {
    selectedDocument: any
    setSelectedDocument: any
    uploadedFile: any
    setUploadedFile: any
    errorText: boolean
    onChange: any
    onClick: any
    fileInputRef: any
    handleDragOver: any
    handleDrop: any
    handleDropFile: any
    details?: any
}

export default function ImageUpload(props: UploadProps) {
    console.log(props.selectedDocument, 'selectedDcuemnt')
    return <div className='upload-container'>
        <label className='input-label'>Upload Image</label>
        {props.selectedDocument.length !== 0
            ? <div className='upload-container-half-width'>
                <div className='dashed-image-wrapper'>
                    <div className='image-wrapper'>
                        <img className='uploaded-img' src={props.selectedDocument[0].src} />
                        <div className='edit-button-wrapper'>
                            <button className='edit-button' onClick={props.onClick}>
                                <img className='edit-icon' src='/edit-icon.svg'/>
                            </button>
                        </div>
                        <input
                            className='file-upload-input'
                            type='file'
                            accept=".jpg,.jpeg,.png"
                            ref={props.fileInputRef}
                            onChange={(e) => {
                                props.onChange(e)
                            }}
                        />
                    </div>
                </div>
            </div>
            : <div className='upload-container-full-width'>
                <div className='dashed-border'>
                    <div className='upload-wrapper' onClick={props.onClick} onDrop={props.handleDrop} onDragOver={props.handleDragOver}>
                        <div className='upload-box'>
                            <div className='doc-details'>
                                <div className='doc-icon'>
                                    <img src='/img-icon.svg'></img>
                                </div>
                                <div className='upload-button-wrapper'>
                                    <button onClick={props.onClick} className='upload-button'>
                                        Click to upload
                                    </button>
                                </div>
                                <div className='doc-type'>
                                    PNG, SVG or JPG
                                </div>
                                <div className='doc-size'>
                                    (472 x 190)
                                </div>
                                
                                <div className='upload-action'>
                                <input
                                        className='file-upload-input'
                                        type='file'
                                        accept=".jpg,.jpeg,.png"
                                        ref={props.fileInputRef}
                                        onChange={(e) => {
                                            props.onChange(e)
                                        }}
                                    /> 
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        }
    </div>
}