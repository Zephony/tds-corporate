'use client';

import SiteHeader from '@/components/SiteHeader';

export default function MobileKycPage() {
  return (
    <>
      <SiteHeader />
      <section className="mk-hero">
        <div className="mk-container">
        <div className="mk-hero-grid">
          <div className="mk-hero-content">
            <h1 className="mk-hero-title">
              Carrier-derived Mobile KYC &amp; Trust Scoring
              <span> approved in seconds </span>
            </h1>
            <p className="mk-hero-paragraph">
              Identify fraud, verify identity, and reduce risk 
              using mobile network signals — with instant onboarding 
              and transparent pricing.
            </p>
            <p className="mk-hero-paragraph">
              Built for fraud prevention, lead validation, and 
              high-risk customer journeys.
            </p>
            
            <div className="mk-hero-buttons">
              <a href="#" className="mk-btn-primary">Get Started → </a>
              <a href="#" className="mk-btn-secondary">View API Docs → </a>
            </div>
          </div>
          <div className="mk-hero-visual">
            <div className="mk-hero-visual-placeholder"></div>
          </div>
        </div>
        </div>
      </section>
    </>
  );
}