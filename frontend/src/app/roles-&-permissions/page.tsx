'use client'
import { useState } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

import { getCollectionSearchParamsFromPage } from '@/helpers'
import { copy } from '@/helpers'
import { replaceUnderScoreWithSpace } from '@/helpers'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'
import useRequest from '@/hooks/useRequest'
import '@/css/pages/settings.css'

// Form initial Data for Users
const initialUpdateUserData = {
    name: '',
    email: '',
    id_role: '',
 
}

// Form initial Data for Users
const initialAddUserData = {
    name: '',
    email: '',
    id_role: '',
}

// Form initial Data for Roles
const initialUpdateRoleData = {
    name: '',
    permission: '',
}

// Form initial Data for Roles
const initialAddRoleData = {
    name: '',
    permission: '',
}

// Hardcoded user data with all details - using values from the table
const hardcodedUsersData = [
    {
        id: 1,
        name: 'Miksa Fruzsina',
        email: 'miksafru@hotmail.com',
        role: 'Campaign Manager',
        role_details: { name: 'Campaign Manager' },
        status: 'Active',
        support_flags: 0,
        employee_id: 1029,
        phone: '+44 3445259349',
        address: '88 Lamington St, Teneriffe EC88 1BP',
        joined_on: 'Nov 3, 2023',
        ni_number: 'QQ 12 34 56 C',
        gender: 'Male',
        date_of_birth: 'Apr 12, 1992',
        nationality: 'British',
        profile_image: '/admin-dp.svg',
        activity_logs: [
            { id: 1, date: 'Jan 2, 2025', login_at: '9:01', logout_at: '18:12', duration: '9h 11m' },
            { id: 2, date: 'Jan 3, 2025', login_at: '7:39', logout_at: '14:33', duration: '7h 23m' },
            { id: 3, date: 'Jan 4, 2025', login_at: '8:54', logout_at: '16:45', duration: '8h 11m' },
            { id: 4, date: 'Jan 5, 2025', login_at: '6:11', logout_at: '13:01', duration: '7h 10m' },
            { id: 5, date: 'Jan 6, 2025', login_at: '2:27', logout_at: '8:00', duration: '6h 27m' },
            { id: 6, date: 'Jan 7, 2025', login_at: '-', logout_at: '-', duration: '-' },
            { id: 7, date: 'Jan 8, 2025', login_at: '9:01', logout_at: '18:12', duration: '9h 11m' },
        ],
        active_hours: '29h 21m',
        inactive_hours: '8h 2m',
        payroll: {
            salary_pay_rate: '£2000/month',
            bank_name: 'Barclays',
            account_number: '12345678',
            probation_period: '3 months',
            working_hours: '37.5 hours/week',
            holiday_entitlement: '25 days + bank holidays'
        }
    },
    {
        id: 2,
        name: 'Szűts Gabriella',
        email: 'szűts_gabi@gmail.com',
        role: 'Admin',
        role_details: { name: 'Admin' },
        status: 'Active',
        support_flags: 1,
        employee_id: 1030,
        phone: '+44 3445259348',
        address: '123 Main St, London SW1A 1AA',
        joined_on: 'Jan 15, 2024',
        ni_number: 'AB 11 22 33 D',
        gender: 'Female',
        date_of_birth: 'Mar 20, 1990',
        nationality: 'British',
        profile_image: '/admin-dp.svg',
        activity_logs: [
            { id: 8, date: 'Jan 2, 2025', login_at: '8:30', logout_at: '17:45', duration: '9h 15m' },
            { id: 9, date: 'Jan 3, 2025', login_at: '8:45', logout_at: '17:30', duration: '8h 45m' },
            { id: 10, date: 'Jan 4, 2025', login_at: '9:00', logout_at: '18:00', duration: '9h 0m' },
        ],
        active_hours: '27h 0m',
        inactive_hours: '10h 23m',
        payroll: {
            salary_pay_rate: '£2500/month',
            bank_name: 'HSBC',
            account_number: '87654321',
            probation_period: '6 months',
            working_hours: '40 hours/week',
            holiday_entitlement: '28 days + bank holidays'
        }
    },
    {
        id: 3,
        name: 'Surány Izabella',
        email: 'surány@hotmail.com',
        role: 'Developer',
        role_details: { name: 'Developer' },
        status: 'Active',
        support_flags: 3,
        employee_id: 1031,
        phone: '+44 3445259347',
        address: '456 Tech Street, London SW1A 2BB',
        joined_on: 'Feb 10, 2024',
        ni_number: 'CD 22 33 44 E',
        gender: 'Female',
        date_of_birth: 'Jun 15, 1991',
        nationality: 'British',
        profile_image: '/admin-dp.svg',
        activity_logs: [
            { id: 11, date: 'Jan 2, 2025', login_at: '8:00', logout_at: '17:00', duration: '9h 0m' },
            { id: 12, date: 'Jan 3, 2025', login_at: '8:15', logout_at: '17:30', duration: '9h 15m' },
            { id: 13, date: 'Jan 4, 2025', login_at: '8:30', logout_at: '18:00', duration: '9h 30m' },
        ],
        active_hours: '27h 45m',
        inactive_hours: '9h 38m',
        payroll: {
            salary_pay_rate: '£3000/month',
            bank_name: 'Lloyds',
            account_number: '11223344',
            probation_period: '3 months',
            working_hours: '40 hours/week',
            holiday_entitlement: '25 days + bank holidays'
        }
    },
    {
        id: 4,
        name: 'Soós Annamária',
        email: 'annamária@live.com',
        role: 'Viewer',
        role_details: { name: 'Viewer' },
        status: 'Active',
        support_flags: 1,
        employee_id: 1032,
        phone: '+44 3445259346',
        address: '789 View Lane, London SW1A 3CC',
        joined_on: 'Mar 5, 2024',
        ni_number: 'EF 33 44 55 F',
        gender: 'Female',
        date_of_birth: 'Aug 22, 1993',
        nationality: 'British',
        profile_image: '/admin-dp.svg',
        activity_logs: [
            { id: 14, date: 'Jan 2, 2025', login_at: '9:15', logout_at: '17:30', duration: '8h 15m' },
            { id: 15, date: 'Jan 3, 2025', login_at: '9:00', logout_at: '17:00', duration: '8h 0m' },
            { id: 16, date: 'Jan 4, 2025', login_at: '9:30', logout_at: '17:45', duration: '8h 15m' },
        ],
        active_hours: '24h 30m',
        inactive_hours: '12h 53m',
        payroll: {
            salary_pay_rate: '£1800/month',
            bank_name: 'NatWest',
            account_number: '55667788',
            probation_period: '3 months',
            working_hours: '37.5 hours/week',
            holiday_entitlement: '25 days + bank holidays'
        }
    },
    {
        id: 5,
        name: 'Illés Éva',
        email: 'illés_eva@gmail.com',
        role: 'Viewer',
        role_details: { name: 'Viewer' },
        status: 'Deactivated',
        support_flags: 0,
        employee_id: 1033,
        phone: '+44 3445259345',
        address: '321 Inactive Road, London SW1A 4DD',
        joined_on: 'Apr 12, 2024',
        ni_number: 'GH 44 55 66 G',
        gender: 'Female',
        date_of_birth: 'Dec 5, 1994',
        nationality: 'British',
        profile_image: '/admin-dp.svg',
        activity_logs: [
            { id: 17, date: 'Jan 2, 2025', login_at: '-', logout_at: '-', duration: '-' },
            { id: 18, date: 'Jan 3, 2025', login_at: '-', logout_at: '-', duration: '-' },
            { id: 19, date: 'Jan 4, 2025', login_at: '-', logout_at: '-', duration: '-' },
        ],
        active_hours: '0h 0m',
        inactive_hours: '40h 0m',
        payroll: {
            salary_pay_rate: '£1800/month',
            bank_name: 'Santander',
            account_number: '99887766',
            probation_period: '3 months',
            working_hours: '37.5 hours/week',
            holiday_entitlement: '25 days + bank holidays'
        }
    }
]

// Hardcoded permissions data from API
const hardcodedPermissionsData = [
    { id: 1, name: "Read role", permission_bit: "1" },
    { id: 2, name: "Create role", permission_bit: "2" },
    { id: 3, name: "Update role", permission_bit: "4" },
    { id: 4, name: "Update permissions for role", permission_bit: "8" },
    { id: 5, name: "Delete role", permission_bit: "16" },
    { id: 6, name: "Read permission", permission_bit: "32" },
    { id: 7, name: "Read user", permission_bit: "64" },
    { id: 8, name: "Create user", permission_bit: "128" },
    { id: 9, name: "Update user", permission_bit: "256" },
    { id: 10, name: "Deactivate user", permission_bit: "512" },
    { id: 11, name: "Read vehicle", permission_bit: "1024" },
    { id: 12, name: "Create vehicle", permission_bit: "2048" },
    { id: 13, name: "Update vehicle", permission_bit: "4096" },
    { id: 14, name: "Archive vehicle", permission_bit: "8192" },
    { id: 15, name: "Delete vehicle", permission_bit: "16384" },
    { id: 16, name: "Assign volunteer to vehicle", permission_bit: "32768" },
    { id: 17, name: "Read vehicle statistics", permission_bit: "65536" },
    { id: 18, name: "View previous versions of vehicle", permission_bit: "131072" },
    { id: 19, name: "Read volunteer", permission_bit: "262144" },
    { id: 20, name: "Create volunteer", permission_bit: "524288" },
    { id: 21, name: "Update volunteer", permission_bit: "1048576" },
    { id: 22, name: "Archive volunteer", permission_bit: "2097152" },
    { id: 23, name: "Delete volunteer", permission_bit: "4194304" },
    { id: 24, name: "Read volunteer statistics", permission_bit: "8388608" },
    { id: 25, name: "View previous versions of volunteer", permission_bit: "16777216" },
    { id: 26, name: "Read client", permission_bit: "33554432" },
    { id: 27, name: "Create client", permission_bit: "67108864" },
    { id: 28, name: "Update client", permission_bit: "134217728" },
    { id: 29, name: "Archive client", permission_bit: "268435456" },
    { id: 30, name: "Delete client", permission_bit: "536870912" },
    { id: 31, name: "Read client statistics", permission_bit: "1073741824" },
    { id: 32, name: "View previous versions of client", permission_bit: "2147483648" },
    { id: 33, name: "Read booking", permission_bit: "4294967296" },
    { id: 34, name: "Create booking", permission_bit: "8589934592" },
    { id: 35, name: "Update booking", permission_bit: "17179869184" },
    { id: 36, name: "Cancel booking", permission_bit: "34359738368" },
    { id: 37, name: "View previous versions of booking", permission_bit: "68719476736" },
    { id: 38, name: "Generate different reports", permission_bit: "137438953472" },
    { id: 39, name: "Read previously generated reports", permission_bit: "274877906944" },
    { id: 40, name: "Read and update notification as read", permission_bit: "549755813888" },
    { id: 41, name: "Read activity logs of users", permission_bit: "1099511627776" },
    { id: 42, name: "Read all organization details", permission_bit: "2199023255552" },
    { id: 43, name: "Create a organization", permission_bit: "4398046511104" },
    { id: 44, name: "Update organization details", permission_bit: "8796093022208" },
    { id: 45, name: "Deactivate any organization", permission_bit: "17592186044416" },
    { id: 46, name: "Disable the organization", permission_bit: "35184372088832" },
    { id: 47, name: "Update the organization of admin", permission_bit: "70368744177664" },
    { id: 48, name: "Update the organization of admin", permission_bit: "140737488355328" },
]

// Hardcoded roles data with permissions
const hardcodedRolesData = [
    {
        id: 1,
        name: 'Admin',
        permission_bit_sequence: '2147483647', // Example: includes many permissions
        permissions: [
            'Read role',
            'Create role',
            'Update role',
            'Update permissions for role',
            'Delete role',
            'Read permission',
            'Read user',
            'Create user',
            'Update user',
            'Deactivate user',
            'Read vehicle',
            'Create vehicle',
            'Update vehicle',
            'Archive vehicle',
            'Delete vehicle',
            'Assign volunteer to vehicle',
            'Read vehicle statistics',
            'View previous versions of vehicle',
            'Read volunteer',
            'Create volunteer',
            'Update volunteer',
            'Archive volunteer',
            'Delete volunteer',
            'Read volunteer statistics',
            'View previous versions of volunteer',
            'Read client',
            'Create client',
            'Update client',
            'Archive client',
            'Delete client',
            'Read client statistics',
            'View previous versions of client',
            'Read booking',
            'Create booking',
            'Update booking',
            'Cancel booking',
            'View previous versions of booking',
            'Generate different reports',
            'Read previously generated reports',
            'Read and update notification as read',
            'Read activity logs of users',
            'Read all organization details',
            'Create a organization',
            'Update organization details',
            'Deactivate any organization',
            'Disable the organization',
            'Update the organization of admin'
        ]
    },
    {
        id: 2,
        name: 'Campaign Manager',
        permission_bit_sequence: '1073741823',
        permissions: [
            'Read role',
            'Create role',
            'Update role',
            'Read permission',
            'Read user',
            'Create user',
            'Update user',
            'Read vehicle',
            'Create vehicle',
            'Update vehicle',
            'Read volunteer',
            'Create volunteer',
            'Update volunteer',
            'Read client',
            'Create client',
            'Update client',
            'Read booking',
            'Create booking',
            'Update booking',
            'Cancel booking',
            'Generate different reports',
            'Read previously generated reports',
            'Read and update notification as read',
            'Read activity logs of users'
        ]
    },
    {
        id: 3,
        name: 'Developer',
        permission_bit_sequence: '536870911',
        permissions: [
            'Read role',
            'Create role',
            'Update role',
            'Read permission',
            'Read user',
            'Create user',
            'Update user',
            'Read vehicle',
            'Create vehicle',
            'Update vehicle',
            'Read volunteer',
            'Create volunteer',
            'Update volunteer',
            'Read client',
            'Create client',
            'Update client',
            'Read booking',
            'Create booking',
            'Update booking'
        ]
    },
    {
        id: 4,
        name: 'Viewer',
        permission_bit_sequence: '63',
        permissions: [
            'Read role',
            'Read permission',
            'Read user',
            'Read vehicle',
            'Read volunteer',
            'Read client',
            'Read booking'
        ]
    }
]

export default function RolesAndPermissions() {
    const { request } = useRequest()

    // Set query params
    const [queryParams, setQueryParam] = useQueryParams()

    // Stores Users data
    const [usersC, updateUsersC] = useCollection('admin/users', null, null)

    // Stores Roles data
    const [rolesC, updateRolesC] = useCollection('admin/roles', null, null)

    // Toggle states
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()
    const [showUserRightSidePanel, toggleUserRightSidePanel] = useToggle()
    const [showRoleRightSidePanel, toggleRoleRightSidePanel] = useToggle()

    // Store clicked item index
    const [clickedUserIndex, setClickedUserIndex] = useState()
    const [clickedRoleIndex, setClickedRoleIndex] = useState()
    const [userIndex, setUserIndex] = useState()
    const [roleIndex, setRoleIndex] = useState()
    const [userDetails, setUserDetails] = useState()
    const [roleDetails, setRoleDetails] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()
    const [activeTable, setActiveTable] = useState('users') // 'users' or 'roles'
    const [expandedPermissions, setExpandedPermissions] = useState({})
    
    // Tabs configuration for users
    const [tabs, setTabs] = useState({
        'view': {
            'basic_details': {
                label: 'Basic Details'
            },
            'activity_log': {
                label: 'Activity Log'
            },
            'payroll': {
                label: 'Payroll'
            },
        },
        'edit': {
            'basic_details': {
                label: 'Basic Details'
            },
        }
    })
    
    // Active tab state
    const [activeTab, setActiveTab] = useState('basic_details')

    // Delete modal states
    const [deleteModalTitle, setDeleteModalTitle] = useState()
    const [deleteModalDescription, setDeleteModalDescription] = useState()
    const [deleteBtn, setDeleteBtn] = useState()
    const [itemToDelete, setItemToDelete] = useState()
    const [deleteType, setDeleteType] = useState() // 'user' or 'role'

    // Message state
    const [message, setMessage] = useState([])

    // Form states for Users
    const [
        addUserData,
        setAddUserData,
        onAddUserDataInputChange,
        addUserDataErrors,
        setAddUserDataErrorsMap,
        addUserDataErrorMessage,
        setAddUserDataErrorMessage,
    ] = useForm(copy(initialAddUserData))

    const [
        updateUserData,
        setUpdateUserData,
        onUpdateUserDataInputChange,
        updateUserDataErrors,
        setUpdateUserDataErrorsMap,
        updateUserDataErrorMessage,
        setUpdateUserDataErrorMessage,
    ] = useForm(copy(initialUpdateUserData))

    // Form states for Roles
    const [
        addRoleData,
        setAddRoleData,
        onAddRoleDataInputChange,
        addRoleDataErrors,
        setAddRoleDataErrorsMap,
        addRoleDataErrorMessage,
        setAddRoleDataErrorMessage,
    ] = useForm(copy(initialAddRoleData))

    const [
        updateRoleData,
        setUpdateRoleData,
        onUpdateRoleDataInputChange,
        updateRoleDataErrors,
        setUpdateRoleDataErrorsMap,
        updateRoleDataErrorMessage,
        setUpdateRoleDataErrorMessage,
    ] = useForm(copy(initialUpdateRoleData))

    // Activity Log table columns
    const [activityLogColumns] = useState([
        {
            name: 'Date',
            id: 'date',
            visible: true,
            sortable: false,
            render: row => (
                <div className='activity-log-date'>{row?.date || '--'}</div>
            )
        },
        {
            name: 'Login at',
            id: 'login_at',
            visible: true,
            sortable: false,
            render: row => (
                <div className='activity-log-login'>{row?.login_at || '--'}</div>
            )
        },
        {
            name: 'Logout at',
            id: 'logout_at',
            visible: true,
            sortable: false,
            render: row => (
                <div className='activity-log-logout'>{row?.logout_at || '--'}</div>
            )
        },
        {
            name: 'Duration',
            id: 'duration',
            visible: true,
            sortable: false,
            render: row => (
                <div className='activity-log-duration'>{row?.duration || '--'}</div>
            )
        }
    ])

    // Users table columns
    const [userColumns] = useState([
        {
            name: 'No',
            id: 's_no',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => (
                <div className='s-no'>{index + 1}</div>
            )
        },
        {
            name: 'Name',
            id: 'name',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='user-name'>
                    <div className='name-avatar' style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <img src='/admin-dp.svg' alt='User' />
                        <span className='name'>{row?.name}</span>
                    </div>
                </div>
            )
        },
        {
            name: 'Email',
            id: 'email',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='email'>{row?.email}</div>
            )
        },
        {
            name: 'Role',
            id: 'role',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='role'>{row?.role_details?.name || 'N/A'}</div>
            )
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='status-main'>
                    <div className={`status-${row?.status === 'Active' || row?.status === 'ACTIVE' ? 'green' : 'grey'}`}>
                        {row?.status === 'Active' || row?.status === 'ACTIVE' ? 'Active' : row?.status === 'Deactivated' || row?.status === 'DEACTIVATED' ? 'Deactivated' : row?.status}
                    </div>
                </div>
            )
        },
        {
            name: 'Support Flags',
            id: 'support_flags',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='support-flags'>{row?.support_flags || 0}</div>
            )
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            render: (row, customData, collection, updateCollection, index) => (
                <div className='action'>
                    <div className='action-button'>
                        <button
                            onClick={(e) => {
                                e.stopPropagation()
                                if (row?.status === 'active' || row?.status === 'Active' || row?.status === 'ACTIVE') {
                                    handleDeactivateUser(e, row.id)
                                } else {
                                    handleActivateUser(e, row.id)
                                }
                            }}
                            className={`status-no-bg ${
                                row?.status === 'Active' || row?.status === 'ACTIVE' ? 'red-no-bg' : 'blue-no-bg'
                            }`}
                        >
                            {row?.status === 'Active' || row?.status === 'ACTIVE' ? 'Deactivate' : 'Activate'}
                        </button>
                        <button
                            onClick={(e) => {
                                e.stopPropagation()
                                setActiveTable('users')
                                setViewMode('edit')
                                toggleUserRightSidePanel()
                                setClickedUserIndex(index)
                                setUpdateUserData({
                                    name: row.name,
                                    email: row.email,
                                    id_role: row.id_role || '',
                                    status: row.status,
                                })
                            }}
                            className='edit-icon-wrapper'
                        >
                            <img
                                className='edit-icon'
                                src='/edit-icon.svg'
                                alt='Edit'
                            />
                        </button>
                    </div>
                </div>
            )
        },
    ])

    // Roles table columns
    const roleColumns = [
        {
            name: 'No',
            id: 's_no',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => (
                <div className='s-no'>{index + 1}</div>
            )
        },
        {
            name: 'Role',
            id: 'name',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='role-name'>{row?.name}</div>
            )
        },
        {
            name: 'No. of Users',
            id: 'user_count',
            visible: true,
            sortable: 'backend',
            render: row => {
                // Count users with this role from hardcoded data
                const userCount = hardcodedUsersData.filter(user => user.role_details?.name === row.name).length
                return <div className='user-count'>{userCount}</div>
            }
        },
        {
            name: 'Permissions',
            id: 'permissions',
            visible: true,
            sortable: false,
            render: row => {
                // Get permissions from hardcoded data
                const permissions = getRolePermissions(row) || []
                const rowId = row?.id
                const isExpanded = expandedPermissions[rowId] || false
                const displayPermissions = isExpanded ? permissions : permissions.slice(0, 7)
                const remainingCount = permissions.length - 7

                return (
                    <div className='permissions'>
                        {displayPermissions.map((perm, idx) => (
                            <button key={`${rowId}-${perm}-${idx}`} className='permission-tag'>
                                {perm}
                            </button>
                        ))}
                        {permissions.length > 7 && (
                            <button 
                                className={`permission-tag .more-permissions ${isExpanded ? 'link-like-button' : ''}`}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setExpandedPermissions(prev => {
                                        const newState = {
                                            ...prev,
                                            [rowId]: !prev[rowId]
                                        };
                                        return newState;
                                    });
                                }}
                            >
                                {isExpanded ? 'View less' : `+${remainingCount}`}
                            </button>
                        )}
                    </div>
                )
            }
        },
    ]

    // Helper function to get permissions for a role
    const getRolePermissions = (role) => {
        // Use permissions from hardcoded data if available
        if (role?.permissions && role.permissions.length > 0) {
            return role.permissions
        }
        // Fallback to parsing from permission_bit_sequence if needed
        return []
    }

    // Search functionality for Users
    const handleUserSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)
            return { searchParams }
        })
    }

    // Search functionality for Roles
    const handleRoleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)
            return { searchParams }
        })
    }

    // Display the request status
    const showMessage = (status, text) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    // User CRUD operations
    const handleAddUser = async (e) => {
        e.preventDefault()
        let requestData = copy(addUserData)
        try {
            await request.post('users', requestData)
            updateUsersC({ reload: true })
            setAddUserData(copy(initialAddUserData))
            toggleUserRightSidePanel()
            showMessage('success', 'User created successfully.')
        } catch (err) {
            showMessage('error', 'Failed to create user.')
        }
    }

    const handleUpdateUser = async (e) => {
        e.preventDefault()
        let requestData = copy(updateUserData)
        try {
            await request.patch(`users/${usersC.items[clickedUserIndex].id}`, requestData)
            updateUsersC({ reload: true })
            setUpdateUserData(copy(initialUpdateUserData))
            toggleUserRightSidePanel()
            showMessage('success', 'User updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update user')
        }
    }

    const handleDeleteUser = async (e, id) => {
        e.preventDefault()
        try {
            await request.delete(`users/${id}`)
            updateUsersC({ reload: true })
            toggleDeleteModal()
            showMessage('success', 'User deleted successfully')
        } catch (err) {
            showMessage('error', 'Failed to delete user')
        }
    }

    const handleActivateUser = async (e, id) => {
        e.preventDefault()
        try {
            await request.patch(`users/${id}`, { status: 'active' })
            updateUsersC({ reload: true })
            showMessage('success', 'User activated successfully.')
        } catch (err) {
            showMessage('error', 'Failed to activate user.')
        }
    }

    const handleDeactivateUser = async (e, id) => {
        e.preventDefault()
        try {
            await request.patch(`users/${id}`, { status: 'inactive' })
            updateUsersC({ reload: true })
            showMessage('success', 'User deactivated successfully.')
        } catch (err) {
            showMessage('error', 'Failed to deactivate user.')
        }
    }

    // Role CRUD operations
    const handleAddRole = async (e) => {
        e.preventDefault()
        let requestData = copy(addRoleData)
        try {
            await request.post('roles', requestData)
            updateRolesC({ reload: true })
            setAddRoleData(copy(initialAddRoleData))
            toggleRoleRightSidePanel()
            showMessage('success', 'Role created successfully.')
        } catch (err) {
            showMessage('error', 'Failed to create role.')
        }
    }

    const handleUpdateRole = async (e) => {
        e.preventDefault()
        let requestData = copy(updateRoleData)
        try {
            await request.patch(`roles/${rolesC.items[clickedRoleIndex].id}`, requestData)
            updateRolesC({ reload: true })
            setUpdateRoleData(copy(initialUpdateRoleData))
            toggleRoleRightSidePanel()
            showMessage('success', 'Role updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update role')
        }
    }

    const handleDeleteRole = async (e, id) => {
        e.preventDefault()
        try {
            await request.delete(`roles/${id}`)
            updateRolesC({ reload: true })
            toggleDeleteModal()
            showMessage('success', 'Role deleted successfully')
        } catch (err) {
            showMessage('error', 'Failed to delete role')
        }
    }

    // Store key value pair for Activity Log Summary to pass into KeyValue Component
    const activityLogSummaryDataList = [
        {
            property: 'active_hours',
            value: userDetails?.active_hours || '0h 0m',
            displayKey: 'Active Hours'
        },
        {
            property: 'inactive_hours',
            value: userDetails?.inactive_hours || '0h 0m',
            displayKey: 'Inactive Hours'
        }
    ]

    // Activity Log Date Form
    const initialActivityLogDateForm = {
        from_date: '',
        to_date: ''
    }

    const [
        activityLogDateForm,
        setActivityLogDateForm,
        onActivityLogDateChange,
        activityLogDateErrors,
        setActivityLogDateErrorsMap,
        activityLogDateErrorMessage,
        setActivityLogDateErrorMessage,
    ] = useForm(copy(initialActivityLogDateForm))

    // On table row click
    const onUserRowClick = (e, index) => {
        e.stopPropagation()
        setUserIndex(index)
        // Use hardcoded data
        const userData = hardcodedUsersData[index]
        setUserDetails(userData)
        setViewMode('view')
        setActiveTable('users')
        setActiveTab('basic_details')
        toggleUserRightSidePanel()
    }

    const onRoleRowClick = (e, index) => {
        e.stopPropagation()
        setRoleIndex(index)
        // Use hardcoded data
        const roleData = hardcodedRolesData[index]
        setRoleDetails(roleData)
        setViewMode('view')
        setActiveTable('roles')
        toggleRoleRightSidePanel()
    }

    // Next/Previous button functionality
    function handleNextUser() {
        const newIndex = userIndex + 1
        setUserIndex(newIndex)
        // Use hardcoded data
        const userData = hardcodedUsersData[newIndex]
        setUserDetails(userData)
    }

    function handlePrevUser() {
        const newIndex = userIndex - 1
        setUserIndex(newIndex)
        // Use hardcoded data
        const userData = hardcodedUsersData[newIndex]
        setUserDetails(userData)
    }

    function handleNextRole() {
        const newIndex = roleIndex + 1
        setRoleIndex(newIndex)
        // Use hardcoded data
        const roleData = hardcodedRolesData[newIndex]
        setRoleDetails(roleData)
    }

    function handlePrevRole() {
        const newIndex = roleIndex - 1
        setRoleIndex(newIndex)
        // Use hardcoded data
        const roleData = hardcodedRolesData[newIndex]
        setRoleDetails(roleData)
    }

    return (
        <div className='page-container'>
            <StatusText text={message} />
            <>
                <div className='left-container'>
                    <Menubar />
                </div>
                <div className='main-content'>
                    <Header title='Settings' />
                    <div className='main-content-body'>
                        {/* Users Table Section */}
                        <div className='table-wrapper'>
                            <TablePageHeader
                                title='Users'
                                onSearch={handleUserSearch}
                                onAddClick={true}
                                onExportClick={null}
                                showActionButtons
                                buttonText='+ Add User'
                                toggleRightSidePanel={() => {
                                    setActiveTable('users')
                                    setViewMode('add')
                                    toggleUserRightSidePanel()
                                }}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={hardcodedUsersData}
                                    columns={userColumns}
                                    controlColumns={[]}
                                    loaded={true}
                                    searchParams={usersC.searchParams}
                                    collection={usersC}
                                    onRowClick={onUserRowClick}
                                    updateCollection={updateUsersC}
                                    selectedIndex={userIndex}
                                />
                            </div>
                        </div>

                        {/* Roles & Permissions Table Section */}
                        <div className='table-wrapper' style={{ marginTop: '2rem' }}>
                            <TablePageHeader
                                title='Roles & Permissions'
                                onSearch={handleRoleSearch}
                                onAddClick={true}
                                onExportClick={null}
                                showActionButtons
                                buttonText='+ Add Role'
                                toggleRightSidePanel={() => {
                                    setActiveTable('roles')
                                    setViewMode('add')
                                    toggleRoleRightSidePanel()
                                }}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={hardcodedRolesData}
                                    columns={roleColumns}
                                    controlColumns={[]}
                                    loaded={true}
                                    searchParams={rolesC.searchParams}
                                    collection={rolesC}
                                    onRowClick={onRoleRowClick}
                                    updateCollection={updateRolesC}
                                    selectedIndex={roleIndex}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </>

            {/* Right Side Panel for Users */}
            {showUserRightSidePanel && (
                <div
                    className='overlay'
                    onClick={() => {
                        toggleUserRightSidePanel()
                        setUserIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'User Details'
                                : viewMode === 'edit'
                                    ? 'Edit User'
                                    : viewMode === 'add'
                                        ? 'Add User'
                                        : ''
                        }
                        details={userDetails}
                        setDetails={setUserDetails}
                        tabs={tabs}
                        setTabs={setTabs}
                        activeTab={activeTab}
                        setActiveTab={setActiveTab}
                        buttonOneFunction={
                            viewMode === 'view'
                                ? handlePrevUser
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? toggleUserRightSidePanel
                                    : null
                        }
                        buttonTwoFunction={
                            viewMode === 'view'
                                ? handleNextUser
                                : viewMode === 'edit'
                                    ? handleUpdateUser
                                    : viewMode === 'add'
                                        ? handleAddUser
                                        : null
                        }
                        buttonNameOne='without-bg-btn'
                        buttonNameTwo='with-bg-btn'
                        buttonTextOne={
                            viewMode === 'view'
                                ? 'Previous User'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next User'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleUserRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setUserIndex}
                        index={userIndex}
                        collection={usersC}
                        updateData={
                            viewMode === 'edit'
                                ? updateUserData
                                : viewMode === 'add'
                                    ? addUserData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateUserDataInputChange
                                : viewMode === 'add'
                                    ? onAddUserDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdateUser}
                        onAddDataInputChange={onAddUserDataInputChange}
                        addData={addUserData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateUserData
                                : viewMode === 'add'
                                    ? setAddUserData
                                    : ''
                        }
                        page='user'
                        rolesCollection={rolesC}
                        activityLogColumns={activityLogColumns}
                        activityLogSummaryDataList={activityLogSummaryDataList}
                        activityLogDateForm={activityLogDateForm}
                        onActivityLogDateChange={onActivityLogDateChange}
                    />
                </div>
            )}

            {/* Right Side Panel for Roles */}
            {showRoleRightSidePanel && (
                <div
                    className='overlay'
                    onClick={() => {
                        toggleRoleRightSidePanel()
                        setRoleIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Role Information'
                                : viewMode === 'edit'
                                    ? 'Edit Role'
                                    : viewMode === 'add'
                                        ? 'Add Role'
                                        : ''
                        }
                        details={roleDetails}
                        setDetails={setRoleDetails}
                        buttonOneFunction={
                            viewMode === 'view'
                                ? handlePrevRole
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? toggleRoleRightSidePanel
                                    : null
                        }
                        buttonTwoFunction={
                            viewMode === 'view'
                                ? handleNextRole
                                : viewMode === 'edit'
                                    ? handleUpdateRole
                                    : viewMode === 'add'
                                        ? handleAddRole
                                        : null
                        }
                        buttonNameOne='without-bg-btn'
                        buttonNameTwo='with-bg-btn'
                        buttonTextOne={
                            viewMode === 'view'
                                ? 'Previous Role'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next Role'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRoleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setRoleIndex}
                        index={roleIndex}
                        collection={rolesC}
                        updateData={
                            viewMode === 'edit'
                                ? updateRoleData
                                : viewMode === 'add'
                                    ? addRoleData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateRoleDataInputChange
                                : viewMode === 'add'
                                    ? onAddRoleDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdateRole}
                        onAddDataInputChange={onAddRoleDataInputChange}
                        addData={addRoleData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateRoleData
                                : viewMode === 'add'
                                    ? setAddRoleData
                                    : ''
                        }
                        page='role'
                    />
                </div>
            )}

            {/* Delete Modal */}
            {showDeleteModal && (
                <Modal
                    title={deleteModalTitle}
                    toggleModal={toggleDeleteModal}
                >
                    <DeleteModal
                        toggleDeleteModal={toggleDeleteModal}
                        handleDelete={deleteType === 'user' ? handleDeleteUser : handleDeleteRole}
                        buyerByCompanyId={itemToDelete}
                        text={deleteModalDescription}
                        deleteBtn={deleteBtn}
                    />
                </Modal>
            )}
        </div>
    )
}

