import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const [dark, setDark] = useState(() => localStorage.getItem("theme") === "dark");

  useEffect(() => {
    document.body.classList.toggle("dark-mode", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">Skibidi Stories</Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/create-story">Create Story</Link></li>
        <li><Link to="/create-instagram">Generate Caption</Link></li>
        <li><Link to="/dashboard">Explore Stories</Link></li>
        <li><Link to="/contact-us">Contact Us</Link></li>
      </ul>
      <div className="dashboard-section">
        <button className="dashboard-button">
          <Link to="/dashboard">Dashboard</Link>
        </button>
        <div className="profile-icon">Y</div>
        {/* Add toggle button here */}
        <button
          className="theme-toggle-btn"
          onClick={() => setDark((d) => !d)}
          aria-label="Toggle dark mode"
        >
          {dark ? "🌙" : "🔆"}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
