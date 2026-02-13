'use client';

export default function SiteHeader() {
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
        </div>
      </div>
    </header>
  );
}

