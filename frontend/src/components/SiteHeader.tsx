'use client';

export default function SiteHeader() {
  return (
    <header className="mk-site-header">
      <div className="mk-site-header-inner">
        <div className="mk-hero-header-left">
          <div className="mk-hero-logo">TDS</div>
          <nav aria-label="Primary">
            <ul className="mk-hero-nav mk-hero-nav-left">
              <li>Product</li>
              <li>Pricing</li>
              <li>Docs</li>
              <li>Use cases</li>
              <li>Customers</li>
            </ul>
          </nav>
        </div>
        <div className="mk-hero-header-right">
          <nav aria-label="Secondary">
            <ul className="mk-hero-nav mk-hero-nav-right">
              <li>Security</li>
              <li>Support</li>
              <li>Login</li>
            </ul>
          </nav>
          <a href="#" className="mk-btn-primary mk-hero-try-btn">
            Try for free
          </a>
        </div>
      </div>
    </header>
  );
}

