'use client'

import moment from 'moment';

const byString = function (object, string, value, forceUseValue = false) {
    // console.log('ByString called..');
    // Return `undefined` if not a string
    try {
        string = string.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        string = string.replace(/^\./, '');           // strip a leading dot
    } catch (TypeError) {
        return undefined;
    }

    var nestedKeys = string.split('.');
    // console.log(nestedKeys);
    for (var i = 0, n = nestedKeys.length; i < n; ++i) {
        var key = nestedKeys[i].replace(/\%/, '.');  // To allow for keys with dots in them

        string = string.replace(/^\./, '');           // strip a leading dot

        // If the key represents an array index
        if (!isNaN(key)) {
            key = parseInt(key);
        }

        if (
            (object !== null && key in object) ||
            (Array.isArray(object) && key <= object.length  // To allow assignment of index `0` to empty array
            )
        ) {
            if (value !== undefined && i + 1 === nestedKeys.length) {
                object[key] = value;
            } else if (forceUseValue && i + 1 === nestedKeys.length) {
                object[key] = value;
            } else {
                object = object[key];
            }
        } else {
            return undefined;
        }
    }

    return object;
}

// Doesn't consider functions. Not sure if the order is also
// checked
const equal = function (object1, object2) {
    return JSON.stringify(object1) === JSON.stringify(object2);
}

// Generates JSON object copy - doesn't copy functions
const copy = function (obj) {
    return JSON.parse(JSON.stringify(obj));
}

const getMap = function (list, property, asArray = false, modifyKey = key => key, valueProperty = null) {
    /* If `asArray` is set to `true`, each property has an array */
    /* If `valueProperty` is set, only that property's value is considered, instead
     * of the whole object. */

    let map = {};
    let key;
    list.map((item) => {
        key = modifyKey(item[property]);

        if (asArray) {
            if (!map.hasOwnProperty(key)) {
                map[key] = [];
            }

            if (valueProperty !== null) {
                map[key].push(item[valueProperty]);
            } else {
                map[key].push(item);
            }
        } else {
            if (valueProperty !== null) {
                // console.log(map, key);
                map[key] = item[valueProperty];
            } else {
                map[key] = item;
            }
        }
    });

    return map;
}

const getTime = function (originalTimeString) {
    let timeString;
    // Default hour and minute values
    let defaultHour = 10;
    let hour = defaultHour;
    let defaultMinute = 0;
    let minute = defaultMinute;
    let prefixUsed = '';    // 'AM' or 'PM' or ''

    // Trim out whitespace
    timeString = originalTimeString.trim();

    // Capitalize string
    timeString = timeString.toUpperCase();

    // Get rid of the am/pm prefixes and determine if a 12 hour offset is required
    let addOffset = false;
    if (timeString.includes('AM')) {
        prefixUsed = 'AM';
        let amPosition = timeString.indexOf('AM');
        timeString = timeString.substring(0, amPosition - 1);
    } else if (timeString.includes('PM')) {
        prefixUsed = 'PM';
        let pmPosition = timeString.indexOf('PM');
        timeString = timeString.substring(0, pmPosition - 1);
        addOffset = true;
    }

    // Get the hour and the minute from the string only if the string format is right
    if (timeString.includes(':')) {
        let hourStr = timeString.split(':')[0].trim();
        let minuteStr = timeString.split(':')[1].trim();

        if (/^\d+$/.test(hourStr) && /^\d+$/.test(minuteStr)) {
            hour = parseInt(hourStr);
            minute = parseInt(minuteStr);
        }
    } else {
        let hourStr = timeString.split(':')[0].trim();

        if (/^\d+$/.test(hourStr)) {
            hour = parseInt(hourStr);
        }
    }

    // Edge cases of 12 AM and 12 PM which translate to 00:00 and 12:00 respectively
    if (prefixUsed === 'AM' && hour === 12) {
        hour = 0;
    } else if (prefixUsed === 'PM' && hour === 12) {
        hour = 12;
    } else if (addOffset) {
        hour += 12;
    }

    if (hour > 24 || hour < 0 || minute > 60 || minute < 0) {
        hour = defaultHour;
        minute = defaultMinute;
    }

    // To prepend with `0` for single digit integers
    // https://stackoverflow.com/questions/8043026/how-to-format-numbers-by-prepending-0
    let doubleDigitHourString = ('0' + hour).slice(-2);
    let doubleDigitMinuteString = ('0' + minute).slice(-2);;

    return `${doubleDigitHourString}:${doubleDigitMinuteString}`;
}

function getDayLabel(date,
    requiredDateFormat = 'DD-MM-YYYY',
    currentDateFormat = 'YYYY-MM-DD',
    exceptionLabel = 'Not Available',
    showOnlyDate = false
) {
    /*
        Function expects a moment date object in the format
        example: requiredDateFormat = 'DD - MMM - YYYY'
    */
    let dayLabel = '';

    if (requiredDateFormat === null || requiredDateFormat === undefined) {
        console.warn(`requiredDateForm is '${requiredDateFormat}' in getDayLabel()`)
        requiredDateFormat = 'DD-MM-YYYY';
    }

    //Convert to moment if in string
    date = date instanceof moment
        ? date
        : typeof date === 'string'
            ? moment(date, currentDateFormat)
            : 'Invalid Date Format'
        ;

    if (date === 'Invalid Date Format') {
        return <span className='data-not-available'>{exceptionLabel}</span>;
    }

    //TODO: Temporary code. Should improve code
    if (!showOnlyDate) {
        if (date.isSame(moment(), 'day')) {
            dayLabel = 'Today';
        } else if (moment().subtract(1, 'days').isSame(date, 'day')) {
            dayLabel = 'Yesterday';
        } else if (moment().add(1, 'days').isSame(date, 'day')) {
            dayLabel = 'Tomorrow';
        } else {
            dayLabel = date.format(requiredDateFormat);
        }
    } else {
        dayLabel = date.format(requiredDateFormat);
    }

    return dayLabel;
}

function getCollectionSearchParamsFromPage() {
    // Only access window if we're on the client side
    if (typeof window === 'undefined') {
        return new URLSearchParams()
    }
    
    const q = new URLSearchParams(window.location.search).get('q')
    if (q) {
        return new URLSearchParams({ q })
    }

    return new URLSearchParams()
}

function formatDateTime(dateString) {
    const date = new Date(dateString)
    const formattedDate = date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    })
    const formattedTime = date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    })
    return `${formattedDate} ${formattedTime}`
}

function replaceUnderScoreWithSpace(text) {
    if(typeof text !== 'string') return text
    return text.replace(/_/g, ' ')
}

const getChanges = (previous, current) => {
    // console.log('$$ \n GETCHANGE :: START\n', previous, current);
    // https://stackoverflow.com/a/38277505/4667164

    if (isPrimitive(previous) && isPrimitive(current)) {
        if (previous === current) {
            return 'no-change';
        }

        return current;
    }

    // console.log('$$ Object', previous, current, isObject(previous), isObject(current));
    if (isObject(previous) && isObject(current)) {
        // console.log('$$Inside Object', previous, current);
        let keys = Object.keys(current);

        let diff = {};
        for (let key of keys) {
            //Check if the values is Array and then ignore
            //TODO: Current expectancy is value of key in both previous and current will be same
            //need to handle the same in the future.

            //If key is not existing in the previous object, add it as a difference
            if (previous[key] === undefined) {
                diff[key] = current[key];
                continue;
            }

            //TODO: For arrays temporarily returning the value. Should add better comparison logic
            if (Array.isArray(current[key])) {
                diff[key] = current[key];
            } else {
                let value = getChanges(previous[key], current[key]);

                if (value !== 'no-change') {
                    //To delete value if it's a empty array
                    //TODO: How to handle empty objects
                    if (!(JSON.stringify(value) === '{}')) {
                        diff[key] = value;
                    }
                }
            }
        }

        return diff;
    }
}

// Converts a list of items into Select suitable options
const getOptions = function (list, label = 'name', value = 'value') {
    var options = list.map(item => {
        return {
            name: item[label],
            value: item[value],
        }
    });

    return options;
}

// Converts string to lower case
const toLower = function (str) {
    return str ? str.toLowerCase() : str;
}

// Uses recursion
const removeEmptyKeys = function (obj, emptyValues = [null], ignoreKeysList = []) {
    obj = copy(obj);

    const shouldRemoveEmptyObjects = emptyValues.some(val => JSON.stringify(val) === '{}');
    const shouldRemoveEmptyArrays = emptyValues.some(val => JSON.stringify(val) === '[]');

    for (var key in obj) {
        if (ignoreKeysList.includes(key)) {
            continue;
        }

        if (emptyValues.includes(obj[key])) {
            delete obj[key];
        } else if (typeof obj[key] === 'object') {
            // console.log('Object loop START', key);
            obj[key] = removeEmptyKeys(obj[key], emptyValues, ignoreKeysList);

            // console.log('Object loop', key, obj[key]);

            if ((shouldRemoveEmptyArrays && Array.isArray(obj[key])) && obj[key].length === 0) {
                // console.log('InsideArrayRemove', key, obj[key]);
                delete obj[key];
            } else if (shouldRemoveEmptyObjects && Object.keys(obj[key]).length === 0) {
                // console.log('InsideObjectRemove',key, obj[key]);
                delete obj[key];
            }
            // console.log('Object loop :: END', key, obj[key]);
        }
    }

    return obj;
}

const shortenText = (text) => {
    if (!text) return ""
    if (text.length > 10) {
        return text.slice(0, 10) + '...'
    } else {
        return text
    }
}

const numFormat = function (number, currency, decimalPlaces = 2, language, locale) {
    if (!language) {
        language = lang;
    }

    if (!locale) {
        switch (language) {
            case 'it':
                locale = 'it-IT';
                break;
            default:
                locale = 'en-US';
        }
    }

    return new Intl.NumberFormat(
        locale,
        {
            style: currency ? 'currency' : undefined,
            currency: currency,
            // maximumSignificantDigits: 1,
            minimumFractionDigits: decimalPlaces,
        }
    ).format(number);
}


// Calculate width of the bar chart based on the available space
// Used to display barchart on the details pages (vehicles, volunteers, clients, etc.)
// const getDetailsPageBarChartWidth = (ref) => {
//     const contentWidth = document.querySelector('.app-content.details-view').offsetWidth
//     const leftPageContentWidth = document.querySelector('.left-page-content').offsetWidth
//     const gap = Number(getPropertyValue('.page-content', 'column-gap').slice(0, -2))
//     const sectionLeftPadding = window.getComputedStyle(
//         ref.current.closest('.section')
//     ).getPropertyValue('padding-left').slice(0, -2)
//     const sectionRightPadding = window.getComputedStyle(
//         ref.current.closest('.section')
//     ).getPropertyValue('padding-right').slice(0, -2)
//     const sectionSidePadding = Number(sectionLeftPadding) + Number(sectionRightPadding)

//     return contentWidth
//         - leftPageContentWidth
//         - gap
//         - sectionSidePadding
// }

export {
    byString,
    equal,
    copy,
    getMap,
    getTime,
    getDayLabel,
    getCollectionSearchParamsFromPage,
    formatDateTime,
    replaceUnderScoreWithSpace,
    getChanges,
    removeEmptyKeys,
    getOptions,
    toLower,
    shortenText,
    numFormat,
    // getDetailsPageBarChartWidth
}