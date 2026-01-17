'use client'

import Link from 'next/link'
import { useState, useRef, useEffect } from 'react'

import { usePathname } from 'next/navigation'

const initialMenuItems = [
    {
        id: 1,
        title: 'Dashboard',
        url: '/',
        icon: '/dashboard-icon.svg',
        iconActive: '/dashboard-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 2,
        title: 'Users',
        url: null,
        icon: '/users-icon.svg',
        iconActive:'/users-active-icon.svg',
        subMenu: [
            {
                title: 'Buyers',
                url: '/buyers',
                isSelected: false
            },
            {
                title: 'Sellers',
                url: '/sellers',
                isSelected: false
            },
            {
                title: 'Due Dilligence',
                url: '/due-dilligence',
                isSelected: false
            },
            {
                title: 'Advertisers',
                url: '/advertisers',
                isSelected: false
            }
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 3,
        title: 'Products',
        url: '/products',
        icon: '/products-icon.svg',
        iconActive: '/products-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 4,
        title: 'Sales',
        url: null,
        icon: '/sales-icon.svg',
        iconActive: '/dashboard-active-icon.svg',
        subMenu: [
            {
                title: 'Live Leads',
                url:'/live-leads',
                isSelected: false
            },
            {
                title: 'Dataset',
                url: '/dataset',
                isSelected: false
            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 5,
        title: 'Categorization',
        url: null,
        icon: '/categorization-icon.svg',
        iconActive: '/categorization-active-icon.svg',
        subMenu: [
            {
                title: 'Category',
                url: '/category',
                isSelected: false
            },
            {
                title: 'Sub Category',
                url: '/sub-category',
                isSelected: false
            },
            {
                title: 'Selections',
                url: '/selections',
                isSelected: false
            },
            {
                title: 'Headers',
                url: '/headers',
                isSelected: false
            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 6,
        title: 'Reports',
        url: null,
        icon: '/reports-icon.svg',
        iconActive: '/reports-active-icon.svg',
        subMenu: [
            {
                title: 'Buyers',
                url: '/report-buyer',
                isSelected: false
            },
            {
                title: 'Sellers',
                url: '/report-seller',
                isSelected: false
            },
            {
                title: 'Due Dilligence',
                url: '/report-due-dilligence',
                isSelected: false
            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 7,
        title: 'Reviews',
        url: '/reviews',
        icon: '/review-icon.svg',
        iconActive: '/review-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 8,
        title: 'Activity Logs',
        url: '/activity-log',
        icon: '/activity-log-icon.svg',
        iconActive: '/activity-log-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 9,
        title: 'Blog',
        url: '/blog',
        icon: '/blog-icon.svg',
        iconActive: '/blog-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 10,
        title: 'Disputes',
        url: '/disputes',
        icon: '/disputed-icon.svg',
        iconActive: '/disputed-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
    {
        id: 11,
        title: 'Transactions',
        url: null,
        icon: '/transaction-icon.svg',
        iconActive: '/transaction-active-icon.svg',
        subMenu: [
            {
                title: 'Paypal',
                url: '/paypal',
                isSelected: false

            },
            {
                title: 'Boodil',
                url: '/boodil',
                isSelected: false

            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 12,
        title: 'Billing',
        url: '/billing',
        icon: '/billing-icon.svg',
        iconActive: '/billing-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
]

const initialBottomMenuItems = [
    {
        id: 1,
        title: 'Marketing',
        url: null,
        icon: '/marketing-icon.svg',
        iconActive: '/marketing-active-icon.svg',
        subMenu: [
            {
                title: 'Templates',
                url: '/templates',
                isSelected: false
            },
            {
                title: 'Email',
                url: '/email',
                isSelected: false
            },
            {
                title: 'SMS',
                url: '/sms',
                isSelected: false
            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 2,
        title: 'Settings',
        url: null,
        icon: '/settings-icon.svg',
        iconActive: '/settings-active-icon.svg',
        subMenu: [
            {
                title: 'Data Types',
                url: '/data-types',
                isSelected: false
            },
            {
                title: 'Tags',
                url: '/tags',
                isSelected: false
            },
            {
                title: 'Keywords',
                url: '/keywords',
                isSelected: false
            },
            {
                title: 'Commission',
                url: '/commission',
                isSelected: false
            },
            {
                title: 'Roles & Permissions',
                url: '/roles-&-permissions',
                isSelected: false
            },
        ],
        isExpanded: false,
        isSelected: false
    },
    {
        id: 3,
        title: 'Integrations',
        url: '/integrations',
        icon: '/integrations-icon.svg',
        iconActive: '/integrations-active-icon.svg',
        subMenu: [],
        // isExpanded: false,
        isSelected: false
    },
]

export default function Menubar() {
    const [menuItems, setMenuItems] = useState(initialMenuItems)

    const [menuBottomItems, setMenuBottomItems] = useState(initialBottomMenuItems)

    const pathname = usePathname()
    // console.log(pathname, 'pathname')

    // Function to update menu selection based on current pathname
    const updateMenuSelection = (currentPath: string) => {
        console.log('updateMenuSelection called with pathname:', currentPath)
        
        // Update top menu items
        setMenuItems(prev => prev.map(item => {
            // Check if current path matches main menu item
            // Handle root path matching - both '/' and empty string should match dashboard
            const isMatch = item.url === currentPath || 
                           (item.url === '/' && (currentPath === '/' || currentPath === '')) ||
                           (item.url === '' && currentPath === '/')
            
            if (isMatch) {
                console.log('Found matching menu item:', item.title, 'for path:', currentPath)
                return { 
                    ...item, 
                    isSelected: true,
                    isExpanded: false,
                    subMenu: item.subMenu.map(sub => ({ ...sub, isSelected: false }))
                }
            }
            
            // Check if current path matches any submenu item
            const matchingSubMenu = item.subMenu.find(sub => sub.url === currentPath)
            if (matchingSubMenu) {
                return {
                    ...item,
                    isSelected: true, // Select the parent item when submenu is active
                    isExpanded: true,
                    subMenu: item.subMenu.map(sub => ({
                        ...sub,
                        isSelected: sub.url === currentPath
                    }))
                }
            }
            
            // Reset item if no match
            return {
                ...item,
                isSelected: false,
                isExpanded: false,
                subMenu: item.subMenu.map(sub => ({ ...sub, isSelected: false }))
            }
        }))

        // Update bottom menu items
        setMenuBottomItems(prev => prev.map(item => {
            // Check if current path matches main menu item
            // Handle root path matching - both '/' and empty string should match dashboard
            const isMatch = item.url === currentPath || 
                           (item.url === '/' && (currentPath === '/' || currentPath === '')) ||
                           (item.url === '' && currentPath === '/')
            
            if (isMatch) {
                return { 
                    ...item, 
                    isSelected: true,
                    isExpanded: false,
                    subMenu: item.subMenu.map(sub => ({ ...sub, isSelected: false }))
                }
            }
            
            // Check if current path matches any submenu item
            const matchingSubMenu = item.subMenu.find(sub => sub.url === currentPath)
            if (matchingSubMenu) {
                return {
                    ...item,
                    isSelected: true, // Select the parent item when submenu is active
                    isExpanded: true,
                    subMenu: item.subMenu.map(sub => ({
                        ...sub,
                        isSelected: sub.url === currentPath
                    }))
                }
            }
            
            // Reset item if no match
            return {
                ...item,
                isSelected: false,
                isExpanded: false,
                subMenu: item.subMenu.map(sub => ({ ...sub, isSelected: false }))
            }
        }))
    }

    // Update menu selection when pathname changes
    useEffect(() => {
        updateMenuSelection(pathname)
    }, [pathname])

    // Function to set expand and collapse also the menu item to select
    const toggleMenuItem = (
        clickedIndex: number, 
        source: string
    ) => {
        if(source === 'top') {
            setMenuItems(prev =>
                prev.map((item, index) =>
                    index === clickedIndex
                        ? {
                            ...item,
                            isExpanded: !item.isExpanded,
                            isSelected: !item.isSelected
                        }
                        : { 
                            ...item, 
                            isSelected: false,
                            isExpanded: false
                        }
                )
            )
        } else {
            setMenuBottomItems(prev =>
                prev.map((item, index) =>
                    index === clickedIndex
                        ? {
                            ...item,
                            isExpanded: !item.isExpanded,
                            isSelected: !item.isSelected
                        }
                        : {
                            ...item,
                            isSelected: false,
                            isExpanded: false
                        }
                )
            )
        }
    }

    // Function to select SubMenuItems
    const selectSubItem = (
        parentIndex: number, 
        subItemIndex: number,
        source: string
    ) => {
        if(source === 'top') {
            setMenuItems(prev =>
                prev.map((item, index) =>
                    index === parentIndex
                        ? {
                            ...item,
                            subMenu: item.subMenu.map((sub, i) =>
                                i === subItemIndex
                                    ? {
                                        ...sub,
                                        isSelected: sub.isSelected
                                    }
                                    : {
                                        ...sub,
                                        isSelected: sub.isSelected
                                    }
                            )
                        }
                        : item
                )
            )
        } else {
            setMenuBottomItems(prev =>
                prev.map((item, index) =>
                    index === parentIndex
                        ? {
                            ...item,
                            subMenu: item.subMenu.map((sub, i) =>
                                i === subItemIndex
                                    ? {
                                        ...sub,
                                        isSelected: !sub.isSelected
                                    }
                                    : {
                                        ...sub,
                                        isSelected: sub.isSelected
                                    }
                            )
                        }
                        : item
                )
            )
        }

    }

    return <div className='menubar-container'>
        <div className='menubar-top'>
            <div className='menubar-top-logo'>
                <img className='logo-img' src='/logo.png'/>
            </div>

            <div className='menubar-top-text'>
                <div className='menubar-top-title'>
                    TDS
                </div>
                <div className='menubar-top-subtitle'>
                    SuperDash
                </div>
            </div>
        </div>

        <div className="menubar-content">

            <div 
                className='menubar-items'
            >
                {menuItems?.map(
                    (item: any, index: number) => 
                        <div 
                            key={index} 
                            className='menubar-item' 
                            onClick={(e) => {
                                e.stopPropagation()
                                toggleMenuItem(index, 'top')
                            }}
                        >
                            {item?.url
                                ? <Link
                                    href={item?.url}
                                    className={
                                        `menubar-title-item-wrapper 
                                        ${item.isSelected
                                            ? 'menu-selected'
                                            : ''
                                        }
                                    `
                                    }
                                >
                                    <div className='item-icon'>
                                        <img
                                            className='icon-img'
                                            src={item.isSelected
                                                ? item.iconActive
                                                : item.icon
                                            }
                                        />
                                    </div>

                                    <div
                                        className={`menubar-title-item 
                                        ${item.isSelected
                                                ? 'menubar-selected-title'
                                                : ''
                                            }
                                    `}
                                    >
                                        {item.title}
                                    </div>
                                </Link>
                                : <div
                                    className={
                                        `menubar-title-item-wrapper 
                                        ${item.isSelected
                                            ? 'menu-selected'
                                            : ''
                                        }
                                    `
                                    }
                                >
                                    <div className='item-icon'>
                                        <img
                                            className='icon-img'
                                            src={item.isSelected
                                                ? item.iconActive
                                                : item.icon
                                            }
                                        />
                                    </div>

                                    <div
                                        className={`menubar-title-item 
                                        ${item.isSelected
                                                ? 'menubar-selected-title'
                                                : ''
                                            }
                                    `}
                                    >
                                        {item.title}
                                    </div>
                                </div>
                            }


                            {item.isExpanded && item.subMenu.length > 0 &&
                                <div className="menubar-subItem">
                                    {item.subMenu?.map(
                                        (sub: any, subIndex: number) => 
                                        <Link 
                                            href={sub.url}
                                            key={subIndex}
                                            className={`subItem 
                                                ${sub.isSelected 
                                                    ? 'subMenu-selected' 
                                                    : ''
                                                }
                                            `}
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                selectSubItem(index, subIndex, 'top')
                                            }}
                                        >
                                            {sub?.title}
                                        </Link>
                                    )}
                                </div>
                            }
                        </div>
                )}
            </div>

            <div 
                className='menubar-bottom-items'
            >
                {menuBottomItems?.map(
                    (item: any, index: number) =>
                        <div
                            key={index}
                            className='menubar-item'
                            onClick={(e) => {
                                e.stopPropagation()
                                toggleMenuItem(index, 'bottom')
                            }}
                        >
                            {item?.url 
                                ? <Link
                                    href={item.url}
                                    className={
                                        `menubar-title-item-wrapper 
                                        ${item.isSelected
                                            ? 'menu-selected'
                                            : ''
                                        }
                                    `
                                    }
                                >
                                    <div className='item-icon'>
                                        <img
                                            className='icon-img'
                                            src={item.isSelected
                                                ? item.iconActive
                                                : item.icon
                                            }
                                        />
                                    </div>
                                    <div
                                        className={`menubar-title-item 
                                        ${item.isSelected
                                                ? 'menubar-selected-title'
                                                : ''
                                            }
                                    `}
                                    >
                                        {item.title}
                                    </div>
                                </Link>
                                : <div
                                    className={
                                        `menubar-title-item-wrapper 
                                        ${item.isSelected
                                            ? 'menu-selected'
                                            : ''
                                        }
                                    `
                                    }
                                >
                                    <div className='item-icon'>
                                        <img
                                            className='icon-img'
                                            src={item.isSelected
                                                ? item.iconActive
                                                : item.icon
                                            }
                                        />
                                    </div>
                                    <div
                                        className={`menubar-title-item 
                                        ${item.isSelected
                                                ? 'menubar-selected-title'
                                                : ''
                                            }
                                    `}
                                    >
                                        {item.title}
                                    </div>
                                </div>
                            }
                            

                            {
                                item.isExpanded && 
                                item.subMenu.length > 0 &&
                                    <div className="menubar-subItem">
                                        {item.subMenu?.map(
                                            (sub:any, subIndex: number) =>
                                                <Link
                                                    key={subIndex}
                                                    href={sub.url}
                                                    className={`subItem 
                                                        ${sub.isSelected
                                                            ? 'subMenu-selected'
                                                            : ''
                                                        }
                                                    `}
                                                    onClick={(e) => {
                                                        e.stopPropagation()
                                                        selectSubItem(index, subIndex, 'bottom')
                                                    }}
                                                >
                                                    {sub?.title}
                                                </Link>
                                        )}
                                    </div>
                            }
                        </div>
                )}
            </div>
        </div>

        <div className='menubar-admin'>
            <hr className='menubar-line-admin'/>

            <div className='menubar-details-admin'>
                <div className='menubar-profile-admin'>
                    <img 
                        className='admin-dp' 
                        src='./admin-dp.svg'
                    />
                </div>

                <div className='menubar-text-admin'>
                    <div className='menubar-name-admin'>
                        <Link href='/profile'>
                            Nick Gorringe
                        </Link>
                    </div>

                    <div className='menubar-status-admin'>
                        Admin
                    </div>
                </div>

                <button className='logout-btn'>
                    <img 
                        className='logout-icon' 
                        src='log-out-icon.svg'
                    />
                </button>
            </div>
        </div>
    </div>
}