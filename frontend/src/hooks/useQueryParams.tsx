'use client'

import { useState } from 'react'

export default function useQueryParams(queryString='') {
    const [params, setParams] = useState(() => new URLSearchParams(queryString || ''))

    // Automatically update the URL's query string as well
    const setQueryParam = (key, value) => {
        setParams(old => {
            let new_ = new URLSearchParams(old)
            if (value === null || value === undefined) {
                new_.delete(key)
            } else {
                new_.set(key, value)
            }

            const newQueryString = '?' + new_.toString()
            // Only update URL if we're on the client side
            if (typeof window !== 'undefined') {
                window.history.replaceState(null, '', newQueryString)
            }
            return new_
        })
    }

    return [params, setParams, setQueryParam]
}