'use client'

import {useState, useAlert, useContext} from 'react'

import Menubar from '@/components/menuBar'
import Header from '@/components/header'

import { useForm } from '@/hooks/useForm'
import useRequest from '@/hooks/useRequest'

import { Input } from '@/components/form'

import '@/css/pages/profile.css'

export default function Profile() {
    const [isAdmin, setIsAdmin] = useState(false)
    return <div className='page-container'>
        <div className='left-container'>
            <Menubar
            />
        </div>
        <div className='main-content'>
            <Header
                title='Profile'
            />
            <div className='main-content-body'>
                <div className='profile-wrapper'>
                    <div className='profile-container-wrapper'>
                        <div className={`profile-container ${isAdmin ? '' : 'locked'}`}>
                            <div className='profile-header'>
                                Change Password
                            </div>
                            <div className='profile-content'>
                                <div className='profile-edit-wrapper'>
                                    <div className='edit-section'>
                                        <Input
                                            label='New Password'
                                        />
                                        <Input
                                            label='Confirm Password'
                                        />
                                    </div>
                                </div>
                            </div>
                            <div className='profile-action-btn'>
                                <button className='save-button'>Save</button>
                            </div>
                        </div>
                    </div>
                    {!isAdmin && 
                        <div className='locked-container-wrapper'>
                            <div className='locked-container'>
                                <img src='/lock.svg'/>
                                <div className='locked-text'>
                                    This content is locked
                                </div>
                                <div className='locked-action-btn'>
                                    <div className='edit-section'>
                                        <Input
                                            placeholder='Enter current password to reset'
                                        />
                                    </div>
                                    <button onClick={() => setIsAdmin(true)} className='unlock-button'>Unlock</button>
                                </div>
                            </div>
                        </div>
                    }
                </div>
            </div>
        </div>
    </div>

}