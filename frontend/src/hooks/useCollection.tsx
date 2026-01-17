import { useState, useEffect } from 'react';

import useRequest from './useRequest';


export default function useCollection(
    url,
    defaultSearchParams,
    prefetchedItems=null,
) {
    const {request} = useRequest()

    const [collection, setCollection] = useState({
        items: prefetchedItems || [],
        loaded: prefetchedItems ? true : false,
        url: url,
        searchParams: defaultSearchParams || new URLSearchParams(),
        version: 0.0,   // Used to force reload collection - Used Math.random()
    })

    let urlWithQueryString = collection.url
    if (collection.searchParams) {
        urlWithQueryString = `${collection.url}?${collection.searchParams.toString()}`
    }

    useEffect(() => {
        if (urlWithQueryString !== null && !collection.loaded) {
            request.get(urlWithQueryString)
                .then(([status_, data]) => {
                    updateCollection({
                        items: data.data,
                        loaded: true,
                    })

                    return data;
                })
                // .catch(eData => { })
                // .finally((a) => { })
        }

        return () => { }
    }, [
        collection.url,
        collection.searchParams.toString(),
        collection.version,
        collection.loaded,
    ])

    function updateCollection(dictOrFunction) {
        setCollection(old => {
            let dict
            if (typeof dictOrFunction === 'function') {
                dict = dictOrFunction(old)
            } else {
                dict = dictOrFunction
            }

            // Set loaded state as false
            let loaded
            if (typeof dict.loaded === 'boolean') {
                loaded = dict.loaded
            } else if ((dict.url !== undefined && dict.url !== old.url)
                || (
                    dict.searchParams
                    && dict.searchParams.toString() !== old.searchParams.toString()
                )
                || dict.reload) {
                loaded = false
            } else {
                loaded = true
            }

            // let queryString = dict.queryString !== undefined
                // ? dict.queryString
                // : old.queryString
            // let searchParams = new URLSearchParams(queryString)
            return {
                url: dict.url || old.url,
                items: dict.items || old.items,
                loaded: loaded,
                searchParams: dict.searchParams || old.searchParams,
                version: dict.reload ? Math.random() : old.version,
            }
        })
    }

    return [collection, updateCollection]
}