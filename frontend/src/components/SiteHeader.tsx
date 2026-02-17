'use client';

import { useState } from 'react';

export default function SiteHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="mk-site-header">
      <div className="mk-site-header-inner">
        <div className="mk-hero-header-left">
          <div className="mk-hero-logo"><img src="/tds-logo.svg" alt="TDS" /></div>
          <nav aria-label="Primary">
            <ul className="mk-hero-nav mk-hero-nav-left">
              <li>Products</li>
              <li>Partnerships</li>
              <li>Features</li>
              <li>Resources</li>
              <li>Pricing</li>
            </ul>
          </nav>
        </div>
        <div className="mk-hero-header-right">
          <nav aria-label="Secondary">
            <ul className="mk-hero-nav mk-hero-nav-right">
              <li>Talk to Sales</li>
              <li>Contact us</li>
              <li>Login</li>
            </ul>
          </nav>
          <a href="#" className="btn btn-nav-primary">
            Try for Free
          </a>
          <button 
            className={`mk-hamburger-menu ${mobileMenuOpen ? 'open' : ''}`}
            aria-label="Menu"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
      
      {/* Mobile Menu Overlay */}
      <div className={`mk-mobile-menu-overlay ${mobileMenuOpen ? 'open' : ''}`} onClick={() => setMobileMenuOpen(false)}>
        <div className={`mk-mobile-menu ${mobileMenuOpen ? 'open' : ''}`} onClick={(e) => e.stopPropagation()}>
          {/* Mobile Menu Header */}
          <div className="mk-mobile-menu-header">
            <div className="mk-hero-logo"><img src="/tds-logo.svg" alt="TDS" /></div>
            <div className="mk-mobile-menu-actions">
              <span className="mk-mobile-talk-to-sales">Talk to Sales</span>
              <button 
                className="mk-mobile-close"
                aria-label="Close menu"
                onClick={() => setMobileMenuOpen(false)}
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>
          
          {/* Mobile Menu Content */}
          <nav className="mk-mobile-menu-content">
            <ul className="mk-mobile-menu-list">
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Products</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Partnerships</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Features</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Resources</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Pricing</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Contact us</a></li>
              <li><a href="#" onClick={() => setMobileMenuOpen(false)}>Login</a></li>
            </ul>
            <a href="#" className="btn btn-nav-primary mk-mobile-cta" onClick={() => setMobileMenuOpen(false)}>
              Try for Free
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}

