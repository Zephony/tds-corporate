import React from 'react';

// import trl from 'data/translations.json';   // trl - short for translations

const LanguageContext = React.createContext();
const CurrentUserContext = React.createContext();

const lang = 'en';      // Supports `it`

export {
    LanguageContext,
    CurrentUserContext,
    lang,
    // trl,
}