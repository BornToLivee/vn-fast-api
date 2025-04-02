function SearchBar({ searchTerm, onSearch, sortBy, onSort, onAddNovel }) {
    return (
      <div className="search-container">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => onSearch(e.target.value)}
          />
        </div>
        <div className="sort-dropdown">
          <select
            value={sortBy}
            onChange={(e) => onSort(e.target.value)}
          >
            <option value="title">Sort by</option>
            <option value="title">Title</option>
            <option value="date">Date Added</option>
          </select>
        </div>
        <button className="add-button" onClick={onAddNovel}>
          Add Novel
        </button>
      </div>
    );
  }
  
  export default SearchBar;
  