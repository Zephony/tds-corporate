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

      <section className="mk-carrier-strip">
        <div className="mk-container">
          <div className="mk-carrier-header">
            <h2 className="mk-carrier-title">
              Carrier-backed identity verification across UK mobile networks
            </h2>
            <p className="mk-carrier-subtitle">
              Trusted by leading carriers and mobile identity partners.
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
              <h3 className="mk-onboarding-card-title">Single, central approval decision</h3>
              <p className="mk-onboarding-card-desc">Approval is granted or rejected at API creation through a single, central approval flow — not via individual mobile network onboarding.</p>
            </div>
            <div className="mk-onboarding-card">
              <span className="mk-onboarding-num">04</span>
              <h3 className="mk-onboarding-card-title">Immediate access to signals</h3>
              <p className="mk-onboarding-card-desc">Once approved, businesses can run checks instantly via API or manual tools while integration is completed.</p>
            </div>
            <div className="mk-onboarding-center-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Score & Mobile KYC */}
      <section className="mk-section mk-trust-score">
        <div className="mk-container">
          <div className="mk-trust-grid">
            <div className="mk-trust-content">
              <h2 className="mk-section-title">Trust Score &amp; Mobile KYC</h2>
              <p className="mk-section-subtitle">Allocate Checks</p>
              <p className="mk-trust-desc">
                Our trust score combines multiple carrier signals into a single, 
                actionable metric. Use it to make instant decisions on user verification, 
                fraud risk, and account security.
              </p>
              <ul className="mk-trust-features">
                <li>
                  <span className="mk-check-icon">✓</span>
                  SIM swap detection
                </li>
                <li>
                  <span className="mk-check-icon">✓</span>
                  Number tenure verification
                </li>
                <li>
                  <span className="mk-check-icon">✓</span>
                  Device binding confirmation
                </li>
                <li>
                  <span className="mk-check-icon">✓</span>
                  Real-time carrier data
                </li>
              </ul>
            </div>
            <div className="mk-trust-visual">
              <div className="mk-trust-card">
                <div className="mk-trust-card-header">Trust Score</div>
                <div className="mk-trust-card-score">87</div>
                <div className="mk-trust-card-label">High Trust</div>
                <div className="mk-trust-card-bar">
                  <div className="mk-trust-card-bar-fill"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Trust Matters */}
      <section className="mk-section mk-why-trust">
        <div className="mk-container">
          <div className="mk-why-trust-grid">
            <div className="mk-why-trust-visual">
              <div className="mk-diagram">
                <div className="mk-diagram-item mk-diagram-fraud">
                  <span className="mk-diagram-icon">⚠</span>
                  <span>Fraud Attempt</span>
                </div>
                <div className="mk-diagram-arrow">→</div>
                <div className="mk-diagram-item mk-diagram-check">
                  <span className="mk-diagram-icon">🔍</span>
                  <span>TDS Check</span>
                </div>
                <div className="mk-diagram-arrow">→</div>
                <div className="mk-diagram-item mk-diagram-block">
                  <span className="mk-diagram-icon">🛡</span>
                  <span>Blocked</span>
                </div>
              </div>
            </div>
            <div className="mk-why-trust-content">
              <h2 className="mk-section-title">Why Trust Matters (Diagram) Result</h2>
              <p className="mk-trust-desc">
                Traditional verification methods fail to catch sophisticated fraud. 
                Carrier-derived signals provide an additional layer of trust that 
                fraudsters cannot easily bypass.
              </p>
              <p className="mk-trust-desc">
                By validating against real carrier data, you catch SIM swaps, 
                number recycling, and account takeover attempts before they succeed.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Policy Enforcement & Fraud Prevention - Dark Section */}
      <section className="mk-section-dark mk-policy">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title-light">Policy Enforcement &amp; Fraud Prevention</h2>
            <p className="mk-section-subtitle-light">
              Automate your security policies with real-time carrier intelligence
            </p>
          </div>
          <div className="mk-policy-grid">
            <div className="mk-policy-card">
              <div className="mk-policy-card-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <h3 className="mk-policy-card-title">Real-time Blocking</h3>
              <p className="mk-policy-card-desc">Instantly block suspicious numbers based on carrier signals and trust scores.</p>
            </div>
            <div className="mk-policy-card">
              <div className="mk-policy-card-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3 className="mk-policy-card-title">Automated Rules</h3>
              <p className="mk-policy-card-desc">Set custom rules to automatically approve, flag, or reject based on risk level.</p>
            </div>
            <div className="mk-policy-card">
              <div className="mk-policy-card-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3 className="mk-policy-card-title">Layered Security</h3>
              <p className="mk-policy-card-desc">Combine carrier data with your existing fraud prevention stack.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Common Steps to Traditional Verification */}
      <section className="mk-section-dark mk-traditional">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title-light">Common Steps to Traditional Verification</h2>
          </div>
          <div className="mk-traditional-grid">
            <div className="mk-traditional-card">
              <div className="mk-traditional-step">1</div>
              <h3 className="mk-traditional-title">Document Upload</h3>
              <p className="mk-traditional-desc">Users must upload ID documents and wait for manual review.</p>
              <span className="mk-traditional-time">⏱ 2-5 days</span>
            </div>
            <div className="mk-traditional-card">
              <div className="mk-traditional-step">2</div>
              <h3 className="mk-traditional-title">Manual Review</h3>
              <p className="mk-traditional-desc">Staff manually verify documents against databases.</p>
              <span className="mk-traditional-time">⏱ 1-3 days</span>
            </div>
            <div className="mk-traditional-card">
              <div className="mk-traditional-step">3</div>
              <h3 className="mk-traditional-title">SMS OTP</h3>
              <p className="mk-traditional-desc">One-time passwords can be intercepted via SIM swap.</p>
              <span className="mk-traditional-time">⚠ Vulnerable</span>
            </div>
            <div className="mk-traditional-card">
              <div className="mk-traditional-step">4</div>
              <h3 className="mk-traditional-title">Approval</h3>
              <p className="mk-traditional-desc">Finally approved after multiple friction points.</p>
              <span className="mk-traditional-time">⏱ 3-7 days total</span>
            </div>
          </div>
        </div>
      </section>

      {/* Why TDS Mobile KYC is Different */}
      <section className="mk-section mk-different">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Why TDS Mobile KYC is Different</h2>
            <p className="mk-section-subtitle">
              Skip the friction. Get instant, carrier-grade verification.
            </p>
          </div>
          <div className="mk-different-grid">
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3 className="mk-different-title">Instant Results</h3>
              <p className="mk-different-desc">Get verification results in milliseconds, not days.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M8 12L10.5 14.5L16 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3 className="mk-different-title">No Documents</h3>
              <p className="mk-different-desc">No ID uploads, selfies, or manual review required.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22S20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3 className="mk-different-title">SIM Swap Protection</h3>
              <p className="mk-different-desc">Detect SIM swaps and number porting in real-time.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 6V12L16 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <h3 className="mk-different-title">Real-time Data</h3>
              <p className="mk-different-desc">Live carrier data, not stale database lookups.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17 21V19C17 16.7909 15.2091 15 13 15H5C2.79086 15 1 16.7909 1 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M23 21V19C22.9986 17.1771 21.765 15.5857 20 15.13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  <path d="M16 3.13C17.7699 3.58317 19.0078 5.17799 19.0078 7.005C19.0078 8.83201 17.7699 10.4268 16 10.88" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <h3 className="mk-different-title">User Friendly</h3>
              <p className="mk-different-desc">Zero friction for legitimate users.</p>
            </div>
            <div className="mk-different-card">
              <div className="mk-different-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14.7 6.3C14.5168 6.11671 14.2671 6.01328 14.0064 6.01328C13.7457 6.01328 13.496 6.11671 13.3128 6.3L9 10.59L7.71 9.3C7.52671 9.11671 7.27711 9.01328 7.01643 9.01328C6.75575 9.01328 6.50615 9.11671 6.32286 9.3C6.13957 9.48329 6.03614 9.73289 6.03614 9.99357C6.03614 10.2543 6.13957 10.5039 6.32286 10.6871L8.32286 12.6871C8.50615 12.8704 8.75575 12.9739 9.01643 12.9739C9.27711 12.9739 9.52671 12.8704 9.71 12.6871L14.71 7.68714C14.8933 7.50385 14.9967 7.25425 14.9967 6.99357C14.9967 6.73289 14.8933 6.48329 14.71 6.3H14.7Z" fill="currentColor"/>
                  <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="currentColor"/>
                </svg>
              </div>
              <h3 className="mk-different-title">Compliant</h3>
              <p className="mk-different-desc">GDPR and data protection compliant.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Simple, Transparent Pricing */}
      <section className="mk-section mk-pricing">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Simple, Transparent Pricing</h2>
            <p className="mk-section-subtitle">
              Pay only for what you use. No hidden fees, no long-term contracts.
            </p>
          </div>
          <div className="mk-pricing-grid">
            <div className="mk-pricing-card">
              <div className="mk-pricing-header">
                <h3 className="mk-pricing-name">Starter</h3>
                <div className="mk-pricing-price">
                  <span className="mk-pricing-currency">£</span>
                  <span className="mk-pricing-amount">0.05</span>
                  <span className="mk-pricing-period">/check</span>
                </div>
              </div>
              <ul className="mk-pricing-features">
                <li>Up to 1,000 checks/month</li>
                <li>Basic trust score</li>
                <li>Email support</li>
                <li>API access</li>
              </ul>
              <a href="#" className="mk-btn-secondary mk-pricing-btn">Get Started</a>
            </div>
            <div className="mk-pricing-card mk-pricing-card-featured">
              <div className="mk-pricing-badge">Most Popular</div>
              <div className="mk-pricing-header">
                <h3 className="mk-pricing-name">Growth</h3>
                <div className="mk-pricing-price">
                  <span className="mk-pricing-currency">£</span>
                  <span className="mk-pricing-amount">0.03</span>
                  <span className="mk-pricing-period">/check</span>
                </div>
              </div>
              <ul className="mk-pricing-features">
                <li>Up to 50,000 checks/month</li>
                <li>Advanced trust score</li>
                <li>Priority support</li>
                <li>Webhooks &amp; analytics</li>
                <li>Custom rules engine</li>
              </ul>
              <a href="#" className="mk-btn-primary mk-pricing-btn">Get Started</a>
            </div>
            <div className="mk-pricing-card">
              <div className="mk-pricing-header">
                <h3 className="mk-pricing-name">Enterprise</h3>
                <div className="mk-pricing-price">
                  <span className="mk-pricing-amount">Custom</span>
                </div>
              </div>
              <ul className="mk-pricing-features">
                <li>Unlimited checks</li>
                <li>Full carrier data access</li>
                <li>Dedicated support</li>
                <li>SLA guarantee</li>
                <li>Custom integration</li>
              </ul>
              <a href="#" className="mk-btn-secondary mk-pricing-btn">Contact Sales</a>
            </div>
          </div>
        </div>
      </section>

      {/* Integrate With Your Existing Systems */}
      <section className="mk-section mk-integrations">
        <div className="mk-container">
          <div className="mk-section-header">
            <h2 className="mk-section-title">Integrate With Your Existing Systems</h2>
            <p className="mk-section-subtitle">
              Works seamlessly with your current tech stack
            </p>
          </div>
          <div className="mk-integrations-logos">
            <div className="mk-integration-logo">
              <img src="/stripe.svg" alt="Stripe" />
            </div>
            <div className="mk-integration-logo">
              <img src="/paypal.svg" alt="PayPal" />
            </div>
            <div className="mk-integration-logo">
              <img src="/slack.svg" alt="Slack" />
            </div>
            <div className="mk-integration-logo">
              <img src="/zapier.svg" alt="Zapier" />
            </div>
            <div className="mk-integration-logo">
              <img src="/klaviyo.svg" alt="Klaviyo" />
            </div>
            <div className="mk-integration-logo">
              <img src="/reamaze.svg" alt="Reamaze" />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mk-footer">
        <div className="mk-footer-container">
          <div className="mk-footer-grid">
            <div className="mk-footer-brand">
              <div className="mk-footer-logo">TDS</div>
              <p className="mk-footer-tagline">
                Carrier-derived Mobile KYC &amp; Trust Scoring for modern businesses.
              </p>
            </div>
            <div className="mk-footer-links">
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Product</h4>
                <ul>
                  <li><a href="#">Mobile KYC</a></li>
                  <li><a href="#">Trust Score</a></li>
                  <li><a href="#">API Docs</a></li>
                  <li><a href="#">Pricing</a></li>
                </ul>
              </div>
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Company</h4>
                <ul>
                  <li><a href="#">About</a></li>
                  <li><a href="#">Blog</a></li>
                  <li><a href="#">Careers</a></li>
                  <li><a href="#">Contact</a></li>
                </ul>
              </div>
              <div className="mk-footer-column">
                <h4 className="mk-footer-heading">Legal</h4>
                <ul>
                  <li><a href="#">Privacy Policy</a></li>
                  <li><a href="#">Terms of Service</a></li>
                  <li><a href="#">GDPR</a></li>
                  <li><a href="#">Security</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mk-footer-bottom">
            <p className="mk-footer-copyright">© 2024 The Data Supermarket. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
}
