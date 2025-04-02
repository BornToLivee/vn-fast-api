import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import NovelCard from './components/NovelCard';
import Pagination from './components/Pagination';
import AddNovelForm from './forms/AddNovel';
import './App.css';

function App() {
  const [novels, setNovels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('title');
  const [currentPage, setCurrentPage] = useState(1);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    // Запрос к вашему API
    axios.get('http://127.0.0.1:8000/novels/')
      .then(response => {
        setNovels(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке данных:', error);
        setLoading(false);
      });
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const filteredNovels = novels.filter(novel =>
    novel.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (novel.description && novel.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleAddNovel = () => {
    setShowAddForm(true);
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleSort = (sortOption) => {
    setSortBy(sortOption);
    const sortedNovels = [...novels];
    sortedNovels.sort((a, b) => {
      if (sortOption === 'title') {
        return a.title.localeCompare(b.title);
      } else if (sortOption === 'rating') {
        return (b.my_rating || 0) - (a.my_rating || 0);
      }
      return 0;
    });
    setNovels(sortedNovels);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleSubmitNovel = async (data) => {
    try {
        const response = await axios.post(
            `http://127.0.0.1:8000/novels/?vndb_id=${data.vndb_id}`, 
            data.novelData
        );
        setNovels([...novels, response.data]);
        setShowAddForm(false);
    } catch (error) {
        console.error('Error adding novel:', error.response?.data || error);
        alert(error.response?.data?.detail || 'Failed to add novel');
    }
  };

  return (
    <div className="app-container">
      <Header toggleSidebar={toggleSidebar} />
      <Sidebar isOpen={sidebarOpen} />
      
      <div className="main-content">
        <div className="content">
          <h1>My novels</h1>
          
          <SearchBar 
            searchTerm={searchTerm} 
            onSearch={handleSearch} 
            sortBy={sortBy} 
            onSort={handleSort} 
            onAddNovel={handleAddNovel} 
          />
          
          {loading ? (
            <div className="loading">Загрузка...</div>
          ) : (
            <div className="novel-container">
              {filteredNovels.map(novel => (
                <NovelCard 
                  key={novel.id}
                  title={novel.title}
                  imageUrl={novel.image_url}
                  rating={novel.my_rating}
                  status={novel.status}
                />
              ))}
            </div>
          )}
          
          <Pagination 
            currentPage={currentPage} 
            onPageChange={handlePageChange} 
            totalPages={Math.ceil(filteredNovels.length / 10)}
          />
        </div>
      </div>
      {showAddForm && (
        <AddNovelForm 
          onClose={() => setShowAddForm(false)}
          onSubmit={handleSubmitNovel}
        />
      )}
      <Footer />
    </div>
  );
}

export default App;
