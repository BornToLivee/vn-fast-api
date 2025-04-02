import React from 'react';

function Header({ toggleSidebar }) {
    return (
        <header className="header">
            <button className="sidebar-toggle" onClick={toggleSidebar}>☰</button>
            <div className="header-content">
                <div className="header-left">
                    <h1 className="logo">VN Library</h1>
                </div>
                <nav className="header-nav">
                    <ul className="nav-links">
                        <li><a href="#" className="nav-link">Home</a></li>
                        <li><a href="#" className="nav-link">My List</a></li>
                        <li><a href="#" className="nav-link">Browse</a></li>
                        <li><a href="#" className="nav-link">About</a></li>
                    </ul>
                </nav>
                <div className="header-right">
                    <button className="theme-toggle">🌙</button>
                    <button className="profile-btn">Profile</button>
                </div>
            </div>
        </header>
    );
}

export default Header;