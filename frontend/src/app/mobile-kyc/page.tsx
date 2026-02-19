'use client';

import SiteHeader from '@/components/SiteHeader';

export default function MobileKycPage() {
  return (
    <main className="mk-page">
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
              <a href="#" className="btn btn-hero-primary">
                Get Started
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 10H16M16 10L12 6M16 10L12 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </a>
              <a href="#" className="mk-btn-secondary">
                View API Docs
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 10H16M16 10L12 6M16 10L12 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </a>
            </div>
          </div>
          <div className="mk-hero-visual">
            <img src="/right-hero-imagee.svg" alt="Hero visual" className="mk-hero-visual-img" />
          </div>
        </div>
        </div>
      </section>

      <section className="mk-carrier-strip">
        <div className="mk-container">
          <div className="mk-carrier-header">
            <h2 className="mk-carrier-title">
              Carrier-Derived Risk & Identity Signals Across UK Mobile Networks
            </h2>
            <p className="mk-carrier-subtitle">
              Signals are derived from UK mobile networks and accessed through TDS’s 
              centralised compliance and approval framework  without requiring businesses 
              to onboard network by network.
            </p>
          </div>
          <div className="mk-carrier-logos">
            <span className="mk-carrier-logo">
              <img src="/logo-vodafone.svg" alt="Vodafone" />
            </span>
            <span className="mk-carrier-logo">
              <img src="/logo-ee.svg" alt="EE" />
            </span>
            <span className="mk-carrier-logo">
              <img src="/logo-o2.svg" alt="O2" />
            </span>
            <span className="mk-carrier-logo">
              <img src="/logo-3.svg" alt="Three" />
            </span>
            <span className="mk-carrier-logo">
              <img src="/logo-prove.svg" alt="Prove" />
            </span>
          </div>
          <p className="mk-carrier-footer">
            This framework enables fast, controlled access while protecting networks, partners, and end users.
          </p>
        </div>
      </section>

      {/* How Instant Business Onboarding Works */}
      <section className="mk-section mk-onboarding">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">How Instant Business Onboarding Works</h2>
            <p className="mk-section-subtitle">
              Get approved to access TDS in minutes with no manual reviews or delays.
            </p>
          </div>
          <div className="mk-pills">
            <span className="mk-pill">No documents</span>
            <span className="mk-pill">No manual review</span>
            <span className="mk-pill">No delays</span>
            <span className="mk-pill">Fully automated</span>
          </div>
          <div className="mk-onboarding-grid">
            <div className="mk-onboarding-card">
              <span className="mk-onboarding-num">01</span>
              <h3 className="mk-onboarding-card-title">Create an API key</h3>
              <p className="mk-onboarding-card-desc">Businesses sign up, select services, and declare their legal basis and intended use.</p>
            </div>
            <div className="mk-onboarding-card">
              <span className="mk-onboarding-num">02</span>
              <h3 className="mk-onboarding-card-title">Automated compliance</h3>
              <p className="mk-onboarding-card-desc">TDS automatically validates: declared use case (e.g. fraud prevention), legal basis, required privacy policy disclosures, consent language where applicable</p>
            </div>
            <div className="mk-onboarding-card">
              <span className="mk-onboarding-num">03</span>
              <h3 className="mk-onboarding-card-title-three">Single, central approval decision</h3>
              <p className="mk-onboarding-card-desc">Approval is granted or rejected at API creation through a single, central approval flow — not via individual mobile network onboarding.</p>
            </div>
            <div className="mk-onboarding-card">
              <span className="mk-onboarding-num">04</span>
              <h3 className="mk-onboarding-card-title">Immediate access to signals</h3>
              <p className="mk-onboarding-card-desc">Once approved, businesses can run checks instantly via API or manual tools while integration is completed.</p>
            </div>
            <div className="mk-onboarding-center-icon">
              <img src="/shield-user-bold.svg" alt="Shield user" />
            </div>
          </div>
        </div>
      </section>

      {/* Trust Score & Mobile KYC */}
      <section className="mk-section mk-trust-score">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Trust Score &amp; Mobile KYC</h2>
          </div>

          {/* Trust Score Feature Card */}
          <div className="mk-feature-card">
            <div className="mk-feature-card-header">
              <span className="mk-feature-pill">Trust Score (Most Popular)</span>
              <h3 className="mk-feature-card-title mk-feature-title-small">What Trust Score does</h3>
              <p className="mk-feature-card-subtitle">
                Trust Score provides a real-time risk indicator for a mobile number using carrier-derived and behavioural signals.
              </p>
              <p className="mk-feature-card-subtitle">
                It is designed to identify fraud, impersonation, and low-quality submissions before downstream costs are triggered.
              </p>
            </div>

            <div className="mk-feature-card-body">
              <div className="mk-feature-card-content">
                <h4 className="mk-feature-section-title">What Trust Score assesses</h4>
                <ul className="mk-feature-list">
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Recent SIM swap activity and timestamps
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    SIM tenure and recency signals
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Line type and carrier context
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Behavioural and network-derived risk indicators
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Known fraud and misuse patterns
                  </li>
                </ul>

                <p className="mk-feature-text">
                  These signals are combined to produce a clear trust score representing the relative risk of a submission.
                </p>

                <h4 className="mk-feature-section-title">How teams use Trust Score</h4>
                <ul className="mk-feature-bullets">
                  <li>Filter high-risk leads instantly</li>
                  <li>Prevent fraud before credit checks or underwriting</li>
                  <li>Compare quality by source or campaign</li>
                  <li>Prioritise review where risk is elevated</li>
                </ul>

                <h4 className="mk-feature-section-title">Why it&apos;s popular</h4>
                <p className="mk-feature-text">
                  Fast, lightweight, and built for high-volume environments where speed and cost matter.
                </p>
              </div>

              <div className="mk-feature-card-visual">
                <img src="/trust-score.svg" alt="Trust Score Check" className="mk-feature-visual-img" />
              </div>
            </div>
          </div>

          {/* Mobile KYC Feature Card */}
          <div className="mk-feature-card">
            <div className="mk-feature-card-header">
              <span className="mk-feature-pill">Mobile KYC</span>
              <h3 className="mk-feature-card-title mk-feature-title-small">What Mobile KYC does</h3>
              <p className="mk-feature-card-subtitle">
                Mobile KYC performs a deeper identity assessment using mobile network signals to evaluate whether submitted identity details plausibly align with the mobile number provided.
              </p>
              <p className="mk-feature-card-subtitle">
                It helps detect impersonation, synthetic identity, and misuse of personal data.
              </p>
            </div>

            <div className="mk-feature-card-body">
              <div className="mk-feature-card-content">
                <h4 className="mk-feature-section-title">What Mobile KYC assesses</h4>
                <ul className="mk-feature-list">
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Identity match indicators
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Mobile account and number status
                  </li>
                  <li>
                    <span className="mk-check-icon">
                      <img src="/green-check-icon.svg" alt="Check" />
                    </span>
                    Consistency between submitted data and mobile attributes
                  </li>
                </ul>

                <h4 className="mk-feature-section-title">When teams use Mobile KYC</h4>
                <ul className="mk-feature-bullets">
                  <li>Higher-risk transactions</li>
                  <li>Regulated journeys</li>
                  <li>Step-up verification when Trust Score flags risk</li>
                </ul>

                <p className="mk-feature-text mk-feature-note">
                  Mobile KYC is typically used alongside Trust Score, not as a replacement.
                </p>
              </div>

              <div className="mk-feature-card-visual">
                <img src="/mobile-kyc.svg" alt="Mobile KYC Information" className="mk-feature-visual-img" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why This Matters (Beyond Fraud) */}
      <section className="mk-section mk-why-matters">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Why This Matters (Beyond Fraud)</h2>
            <p className="mk-section-subtitle">
              Fraud and low-quality submissions don&apos;t just waste leads.
            </p>
          </div>

          <div className="mk-matters-card">
            <p className="mk-matters-intro">They trigger</p>
            
            <div className="mk-matters-grid">
              <div className="mk-matters-column">
                <div className="mk-matters-item">
                  <span className="mk-matters-icon">
                    <img src="/warning-icon.svg" alt="Warning" />
                  </span>
                  <span className="mk-matters-text">Unnecessary credit checks</span>
                </div>
                <div className="mk-matters-item">
                  <span className="mk-matters-icon">
                    <img src="/warning-icon.svg" alt="Warning" />
                  </span>
                  <span className="mk-matters-text">Reputational and moral risk — especially when real people are affected</span>
                </div>
              </div>
              <div className="mk-matters-column">
                <div className="mk-matters-item">
                  <span className="mk-matters-icon">
                    <img src="/warning-icon.svg" alt="Warning" />
                  </span>
                  <span className="mk-matters-text">Wasted underwriting and review time</span>
                </div>
                <div className="mk-matters-item">
                  <span className="mk-matters-icon">
                    <img src="/warning-icon.svg" alt="Warning" />
                  </span>
                  <span className="mk-matters-text">Incorrect account creation</span>
                </div>
              </div>
            </div>

            <p className="mk-matters-footer">
              Catching risk earlier reduces cost, protects consumers, and prevents damage that can&apos;t easily be undone.
            </p>
          </div>
        </div>
      </section>

      {/* Policy Enforcement & Audit Traceability */}
      <section className="mk-section mk-policy-audit">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Policy Enforcement &amp; Audit Traceability</h2>
            <p className="mk-section-subtitle">
              Access is continuously enforced against approved policy content.
            </p>
          </div>

          <div className="mk-policy-audit-grid">
            <div className="mk-policy-audit-item">
              <p className="mk-policy-audit-text">Privacy policy content is monitored daily</p>
            </div>
            <div className="mk-policy-audit-item">
              <p className="mk-policy-audit-text">If required disclosures change, re-verification is triggered automatically</p>
            </div>
            <div className="mk-policy-audit-item">
              <p className="mk-policy-audit-text">If required content is removed, API access is suspended until resolved</p>
            </div>
            <div className="mk-policy-audit-item">
              <p className="mk-policy-audit-text">Every verification is linked to the exact policy version in force at the time</p>
            </div>
          </div>

          <div className="mk-policy-audit-footer">
            <p className="mk-policy-audit-footer-text">
              This creates a clear, provable audit trail for internal review, partners, and third-party checks.
            </p>
            <p className="mk-policy-audit-disclaimer">
              TDS does not assess full GDPR compliance.
            </p>
            <p className="mk-policy-audit-disclaimer">
              TDS enforces authorised disclosure and use conditions to protect networks, partners, and end users.
            </p>
          </div>
        </div>
      </section>

      {/* Common Gaps In Traditional Verification */}
      <section className="mk-section mk-gaps">
        <div className="mk-gaps-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title-light">Common Gaps In Traditional Verification</h2>
            <p className="mk-section-subtitle-light">
              Move from document-heavy verification to carrier-backed identity checks.
            </p>
          </div>

          <div className="mk-gaps-comparison">
            {/* Problems Card */}
            <div className="mk-gaps-card mk-gaps-card-dark">
              <span className="mk-gaps-pill mk-gaps-pill-red">Problems</span>
              <h3 className="mk-gaps-card-title mk-gaps-card-title-light">Why traditional verification breaks at scale</h3>
              <ul className="mk-gaps-list">
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-warning">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                  </span>
                  <span className="mk-gaps-text-light">Weeks-long onboarding and contracts</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-warning">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                  </span>
                  <span className="mk-gaps-text-light">Network-by-network approvals</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-warning">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                  </span>
                  <span className="mk-gaps-text-light">Volume-based pricing barriers</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-warning">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                  </span>
                  <span className="mk-gaps-text-light">Checks performed after costs are incurred</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-warning">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                  </span>
                  <span className="mk-gaps-text-light">Manual, one-off compliance reviews</span>
                </li>
              </ul>
            </div>

            {/* Solution Card */}
            <div className="mk-gaps-card mk-gaps-card-light">
              <span className="mk-gaps-pill mk-gaps-pill-green">Solution</span>
              <h3 className="mk-gaps-card-title">Verify identity at the source</h3>
              <ul className="mk-gaps-list">
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-check">
                    <img src="/green-check-icon.svg" alt="Check" />
                  </span>
                  <span className="mk-gaps-text">Instant B2B approval to access the service</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-check">
                    <img src="/green-check-icon.svg" alt="Check" />
                  </span>
                  <span className="mk-gaps-text">Verify users using live carrier data</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-check">
                    <img src="/green-check-icon.svg" alt="Check" />
                  </span>
                  <span className="mk-gaps-text">Clear match / no-match results</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-check">
                    <img src="/green-check-icon.svg" alt="Check" />
                  </span>
                  <span className="mk-gaps-text">MNO-approved compliance framework</span>
                </li>
                <li className="mk-gaps-item">
                  <span className="mk-gaps-icon mk-gaps-icon-check">
                    <img src="/green-check-icon.svg" alt="Check" />
                  </span>
                  <span className="mk-gaps-text">Centralised approval and enforcement</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Why TDS Mobile KYC is Different */}
      <section className="mk-section mk-different">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Why TDS Mobile KYC Is Different</h2>
          </div>
          <div className="mk-different-grid">
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <img src="/compliance-enforced.svg" alt="Compliance enforced" />
              </div>
              <h3 className="mk-different-title">Compliance-enforced by design</h3>
              <p className="mk-different-desc">Approval is automated, conditional, and enforced at API creation — not a one-time checkbox.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <img src="/transparent-pricing.svg" alt="Transparent pricing" />
              </div>
              <h3 className="mk-different-title">Transparent pricing</h3>
              <p className="mk-different-desc">Same price for everyone. No contracts. No minimums. No expiry.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <img src="/scale.svg" alt="Built for scale" />
              </div>
              <h3 className="mk-different-title">Built for real-world scale</h3>
              <p className="mk-different-desc">API-first, with manual tools available while teams integrate.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <img src="/central-approval-flow.svg" alt="Central approval flow" />
              </div>
              <h3 className="mk-different-title">Single, central approval flow</h3>
              <p className="mk-different-desc">No individual mobile network onboarding required.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Simple, Transparent Pricing */}
      <section className="mk-section mk-pricing">
        <div className="mk-container">
          <div className="mk-pricing-wrapper">
            <div className="mk-section-header">
              <h2 className="mk-section-title">Simple, Transparent Pricing</h2>
              <p className="mk-section-subtitle">
                Enterprise-grade mobile identity and fraud prevention — without contracts, volume commitments, or expiry tricks.
              </p>
            </div>

            <div className="mk-pricing-cards">
              {/* Trust Score Card */}
              <div className="mk-pricing-card mk-pricing-card-recommended">
                <span className="mk-pricing-badge">Recommended</span>
                <h3 className="mk-pricing-name">Trust Score</h3>
                <p className="mk-pricing-subtitle">Carrier-derived risk scoring</p>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">What it&apos;s for</h4>
                  <ul className="mk-pricing-list">
                    <li>Stop fraud and poor-quality leads before they create cost</li>
                    <li>High-risk journeys in lead generation, finance, and utilities</li>
                    <li>Automated risk decisions using mobile network signals</li>
                  </ul>
                </div>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">What you get</h4>
                  <ul className="mk-pricing-list">
                    <li>SIM swap timestamps</li>
                    <li>Account stability &amp; tenure indicators</li>
                    <li>Network-derived risk signals</li>
                    <li>Designed for fraud prevention (not credit scoring)</li>
                  </ul>
                </div>

                <a href="#" className="mk-pricing-btn-primary">£0.35/per check →</a>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">Why teams choose this</h4>
                  <ul className="mk-pricing-list">
                    <li>No contracts</li>
                    <li>No minimum volumes</li>
                    <li>Credits never expire</li>
                    <li>Same price whether you run 10 checks or 10 million</li>
                  </ul>
                </div>
              </div>

              {/* Mobile KYC Card */}
              <div className="mk-pricing-card">
                <h3 className="mk-pricing-name">Mobile KYC</h3>
                <p className="mk-pricing-subtitle">Identity match only</p>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">What it&apos;s for</h4>
                  <ul className="mk-pricing-list">
                    <li>Confirming a user matches a mobile number</li>
                    <li>Lower-risk identity verification flows</li>
                    <li>Situations where risk scoring isn&apos;t required</li>
                  </ul>
                </div>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">What it does</h4>
                  <ul className="mk-pricing-list">
                    <li>Match / no-match identity confirmation</li>
                    <li>No behavioural or risk scoring</li>
                    <li>Verifies mobile number ownership</li>
                    <li>No fraud context on its own</li>
                  </ul>
                </div>

                <a href="#" className="mk-pricing-btn-primary">£0.45/per check →</a>

                <div className="mk-pricing-section">
                  <h4 className="mk-pricing-section-title">Good to know</h4>
                  <ul className="mk-pricing-list">
                    <li>Typically used alongside Trust Score</li>
                    <li>Less popular on its own</li>
                    <li>Same no-contract, no-expiry terms</li>
                  </ul>
                </div>
              </div>
            </div>

            <p className="mk-pricing-disclaimer">* Does not affect credit files. Used solely for fraud prevention</p>

            <div className="mk-pricing-includes">
              <h4 className="mk-pricing-includes-title">All plans include</h4>
              <div className="mk-pricing-includes-grid">
                <span className="mk-pricing-includes-item">Secure API access</span>
                <span className="mk-pricing-includes-item">Single central approval flow at API creation</span>
                <span className="mk-pricing-includes-item">Automated compliance checks</span>
                <span className="mk-pricing-includes-item">Full audit logs per request</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Integrate With Your Existing Systems */}
      <section className="mk-section mk-integrations">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Integrate With Your Existing Systems</h2>
            <div className="mk-feature-card-subtitle">
              Use Mobile KYC and Trust Score via simple REST APIs or manual tools. Ready to connect with your CRM, onboarding flow, or verification platform.
            </div>
            <div className="mk-feature-card-subtitle">
              Teams can start immediately while integration is completed.
            </div>
          </div>
          <div className="mk-integrations-cta">
            <a href="#" className="mk-btn-primary">View Developer Docs →</a>
          </div>
          <div className="mk-integrations-image">
            <img src="/integration-image.svg" alt="API Integration Documentation" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mk-footer">
        <div className="mk-footer-container">
          <div className="mk-footer-grid">
            <div className="mk-footer-brand">
              <div className="mk-footer-logo"><img src="/tds-logo.svg" alt="TDS" /></div>
              <p className="mk-footer-tagline">
                This is sample text. Trusted by 1,500+ leading companies to reduce fraud and improve consumer experiences, TDS is the world&#39;s most accurate identity verification and authentication platform.
              </p>
              <div className="mk-footer-social">
                <a href="#" aria-label="Facebook">
                  <img src="/fb.svg" alt="Facebook" width="20" height="20" />
                </a>
                <a href="#" aria-label="Instagram">
                  <img src="/ig.svg" alt="Instagram" width="20" height="20" />
                </a>
                <a href="#" aria-label="X">
                  <img src="/x.svg" alt="X" width="20" height="20" />
                </a>
                <a href="#" aria-label="LinkedIn">
                  <img src="/li.svg" alt="LinkedIn" width="20" height="20" />
                </a>
              </div>
            </div>
            <div className="mk-footer-links">
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Product</h4>
                <ul>
                  <li><a href="#">TDS Marketplace</a></li>
                  <li><a href="#">TDS DD Verify</a></li>
                  <li><a href="#">TDS Ads Portal</a></li>
                  <li><a href="#">TDS Compliance Tools</a></li>
                </ul>
              </div>
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Resources</h4>
                <ul>
                  <li><a href="#">API Documentation</a></li>
                  <li><a href="#">Blog</a></li>
                  <li><a href="#">Events</a></li>
                </ul>
              </div>
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Company</h4>
                <ul>
                  <li><a href="#">About Us</a></li>
                  <li><a href="#">Leadership</a></li>
                  <li><a href="#">Partners</a></li>
                  <li><a href="#">Customer Stories</a></li>
                </ul>
              </div>
              <div className="mk-footer-column mk-footer-actions">
                <ul>
                  <li><a href="#">Talk to Sales</a></li>
                  <li><a href="#">Contact us</a></li>
                  <li><a href="#">Login</a></li>
                  <li><a href="#" className="mk-btn-primary mk-footer-cta">Try for Free</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mk-footer-bottom">
            <div className="mk-footer-bottom-links">
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
              <a href="#">Legal &amp; Compliance</a>
              <a href="#">Refund Policy</a>
              <a href="#">TDS Policies</a>
              <a href="#">Manage Cookie Preference</a>
              <a href="#">Do Not Sell or Share My Information</a>
            </div>
            <p className="mk-footer-copyright">© The Data Supermarket Ltd. All Rights Reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
