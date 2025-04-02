function Sidebar({ isOpen }) {
    return (
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Iteme</h2>
        </div>
        <ul className="sidebar-menu">
          <li>Item One</li>
          <li>Item Two</li>
          <li>Item Three</li>
          <li>Item Four</li>
        </ul>
      </div>
    );
  }
  
  export default Sidebar;