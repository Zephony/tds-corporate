# TDS Corporate Frontend

The Next.js frontend for the TDS Corporate website.

## Pages

- `/` - Homepage
- `/mobile-kyc` - Mobile KYC product landing page
- `/product` - Product page

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:8081](http://localhost:8081) to view the site.

## Tech Stack

- **Framework**: Next.js 15.5 (App Router)
- **React**: 19.1
- **Language**: TypeScript
- **Styling**: CSS Modules

## Project Structure

```
src/
├── app/                  # Next.js App Router pages
│   ├── page.tsx         # Homepage
│   ├── mobile-kyc/      # Mobile KYC landing page
│   └── product/         # Product page
├── components/          # Reusable components
├── css/                 # Stylesheets
├── hooks/               # Custom React hooks
└── helpers/             # Utility functions
```
