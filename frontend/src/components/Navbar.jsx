function Navbar({ toggleSidebar }) {
    return (
      <nav className="top-nav">
        <button className="toggle-button" onClick={toggleSidebar}>
          ≡
        </button>
        <div className="nav-links">
          <a href="#">Home</a>
          <a href="#">About</a>
          <a href="#">Services</a>
          <a href="#">Contact</a>
        </div>
      </nav>
    );
  }
  
  export default Navbar;