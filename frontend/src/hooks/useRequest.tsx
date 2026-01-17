'use client'

import { useState } from 'react';

export default function useRequest() {
    const [isLoggedIn, setIsLoggedIn] = useState(false)

    function _getRequestOptions(method, body, headers = {}) {
        const isFormData = body instanceof FormData;

        return {
            method,
            headers: isFormData ? headers : { 'Content-Type': 'application/json', ...headers },
            body: isFormData ? body : body ? JSON.stringify(body) : undefined,
        };
    }

    function _handleResponse(response) {
        return response.text().then(text => {
            const data = text && JSON.parse(text)

            if (!response.ok) {
                const error = data || response.statusText
                return Promise.reject([response.status, error])
            }

            return [response.status, data]
        })
    }

    function fetchWrapper(method: string, url: string, body?: null, headers) {
        const requestOptions = _getRequestOptions(method, body, headers)
        return fetch(`/api/v1/${url}`, requestOptions)
            .then(_handleResponse)
            .catch(err => {
                console.log(err)
                if (err[0] === 401) {
                    setIsLoggedIn(false)
                }
                return Promise.reject(err)
            })
    }

    const request = {
        get: (url, headers = {}) => {
            return fetchWrapper('GET', url, null, headers)
        },
        post: (url, body = null, headers = {}) => {
            return fetchWrapper('POST', url, body, headers)
        },
        patch: (url, body = null, headers = {}) => {
            return fetchWrapper('PATCH', url, body, headers)
        },
        put: (url, body = null, headers = {}) => {
            return fetchWrapper('PUT', url, body, headers)
        },
        delete: (url, body = null, headers = {}) => {
            return fetchWrapper('DELETE', url, body, headers)
        },
        postFormFiles: (url, formData, headers = {}) => {
            // Merge headers with the existing headers
            // headers = { ...headers, 'Content-Type': 'multipart/form-data' };

            return fetchWrapper('POST', url, formData, headers);
        },
    }

    return { request }
}