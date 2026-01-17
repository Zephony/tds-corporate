'use client'

import React, { useState, useEffect } from 'react';

import { copy } from '@/helpers/index'
import { useForm } from './useForm';
import useQueryParams from './useQueryParams';


export default function useFilter(
    allowedFilters,
    updateCollection,
    defaultQueryString,
) {
    // On page load, we get the current filter query params from
    // the URL search params and set queryParams state variable
    // as below. Then we convert and store it in the filterData
    // state variable so that the user can edit it via the filter form.
    //
    // When the user applies the filter, we update the queryParams
    // state variable again so that the URL will be updated. We also
    // send the filter data to the backend via the API.

    const [queryParams, setQueryParams, updateQueryParam] = useQueryParams(
        defaultQueryString,
    )

    const [filterData, setFilterData, onFilterInputChange] = useForm(
        getFilterDataFromSearchParams(),
    );
    const [filterEnabled, setFilterEnabled] = useState(true);

    function getFilterDataFromSearchParams() {
        const filterData = {}

        for (let key in allowedFilters) {

            filterData[key] = {
                name: allowedFilters[key].name,
                type: allowedFilters[key].type,
                value: '',
                operator: allowedFilters[key].operator,
                options: allowedFilters[key].options,
            }

            if (queryParams.has(key)) {
                const allowedFilter = allowedFilters[key]

                if (allowedFilter.type === 'text') {
                    if (queryParams.get(key).startsWith('~')) {
                        filterData[key].value = queryParams.get(key).slice(1)
                        filterData[key].operator = 'contains'
                    } else {
                        filterData[key].value = queryParams.get(key)
                        filterData[key].operator = 'equals'
                    }
                } else if (allowedFilter.type === 'select') {
                    filterData[key].value = queryParams.get(key)
                    filterData[key].operator = 'equals'
                } else if (allowedFilter.type === 'checkbox') {
                    console.log('checkbox')
                    filterData[key].value = queryParams.get(key)
                    filterData[key].operator = 'equals' 
                } else if (allowedFilter.type === 'number') {
                    throw new Error('Number filter type is not supported yet')
                } else if (allowedFilter.type === 'date') {
                    throw new Error('Date filter type is not supported yet')
                } else {
                    throw new Error('Unknown filter type: ' + allowedFilter.type)
                }
            }
        }

        return filterData
    }

    function getSearchParamsFromFilterData() {
        const filterParams = new URLSearchParams()
        for (let key in filterData) {
            if (filterData[key].value) {
                if ('operator' in filterData[key]) {
                    if (filterData[key].operator === 'equals') {
                        filterParams.set(key, filterData[key].value)
                    } else if (filterData[key].operator === 'contains') {
                        filterParams.set(key, '~' + filterData[key].value)
                    } else if (filterData[key].operator === 'lesser_than') {
                        filterParams.set(key, '<' + filterData[key].value)
                    } else if (filterData[key].operator === 'greater_than') {
                        filterParams.set(key, '>' + filterData[key].value)
                    }
                }
            }
        }

        return filterParams
    }

    function applyFilter() {
        setFilterEnabled(false);
        updateCollection({ searchParams: getSearchParamsFromFilterData() });
        setFilterEnabled(true);

        // Clear existing filters from query params
        for (let key in allowedFilters) {
            updateQueryParam(key, undefined)
        }

        // Add new filters to query params
        const filterParams = getSearchParamsFromFilterData()
        for (let [key, value] of filterParams) {
            updateQueryParam(key, value)
        }
    }

    function clearFilter() {
        setFilterEnabled(false);
        updateCollection({ searchParams: new URLSearchParams() });

        // Clear existing filters from query params
        for (let key in allowedFilters) {
            updateQueryParam(key, undefined)
        }

        setFilterData(old => {
            const newData = copy(old)
            for (let key in allowedFilters) {
                newData[key].value = ''
            }
            return newData
        });
        setFilterEnabled(true);
    }

    return [
        filterData,
        filterEnabled,
        getSearchParamsFromFilterData,
        getFilterDataFromSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData,
    ]
}