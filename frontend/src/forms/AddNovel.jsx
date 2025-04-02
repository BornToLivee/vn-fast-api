import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AddNovelForm({ onClose, onSubmit }) {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [selectedNovel, setSelectedNovel] = useState(null);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        status: 'READING',
        language: 'RUSSIAN',
        my_rating: '',
        my_review: ''
    });

    useEffect(() => {
        const debounceTimer = setTimeout(async () => {
            if (searchQuery.length >= 2) {
                setLoading(true);
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/novels/search?query=${searchQuery}`);
                    setSearchResults(response.data);
                } catch (error) {
                    console.error('Error searching novels:', error);
                }
                setLoading(false);
            } else {
                setSearchResults([]);
            }
        }, 500);

        return () => clearTimeout(debounceTimer);
    }, [searchQuery]);

    const handleSelectNovel = (novel) => {
        setSelectedNovel(novel);
        setSearchResults([]);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!selectedNovel) return;
        
        const novelData = {
            status: formData.status,
            language: formData.language,
            my_rating: formData.my_rating ? Number(formData.my_rating) : null,
            my_review: formData.my_review || "",
            tags: []
        };

        onSubmit({
            vndb_id: selectedNovel.id,
            novelData: novelData
        });
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h2>Add New Novel</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>

                {!selectedNovel ? (
                    <div className="search-section">
                        <div className="search-box">
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="Type to search novels..."
                                className="search-input"
                            />
                            {loading && <div className="loading-indicator">Searching...</div>}
                        </div>

                        {searchResults.length > 0 && (
                            <div className="search-results">
                                {searchResults.map((novel) => (
                                    <div 
                                        key={novel.id}
                                        className="search-result-item"
                                        onClick={() => handleSelectNovel(novel)}
                                    >
                                        <img 
                                            src={novel.image_url} 
                                            alt={novel.title}
                                            className="result-image"
                                        />
                                        <div className="result-info">
                                            <h3>{novel.title}</h3>
                                            <p>{novel.id}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ) : (

                    <form onSubmit={handleSubmit} className="add-novel-form">
                        <div className="selected-novel">
                            <img 
                                src={selectedNovel.image_url} 
                                alt={selectedNovel.title}
                                className="selected-novel-image"
                            />
                            <h3>{selectedNovel.title}</h3>
                            <button 
                                type="button" 
                                onClick={() => setSelectedNovel(null)}
                                className="change-novel-btn"
                            >
                                Change Novel
                            </button>
                        </div>

                        <div className="form-group">
                            <label htmlFor="status">Status:</label>
                            <select
                                id="status"
                                value={formData.status}
                                onChange={(e) => setFormData({...formData, status: e.target.value})}
                            >
                                <option value="READING">Reading</option>
                                <option value="COMPLETED">Completed</option>
                                <option value="DROPPED">Dropped</option>
                                <option value="PLANNING">Planning</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="language">Language:</label>
                            <select
                                id="language"
                                value={formData.language}
                                onChange={(e) => setFormData({...formData, language: e.target.value})}
                            >
                                <option value="RUSSIAN">Russian</option>
                                <option value="ENGLISH">English</option>
                                <option value="UKRAINIAN">Ukrainian</option>
                                <option value="OTHER">Other</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="my_rating">Rating:</label>
                            <input
                                type="number"
                                id="my_rating"
                                value={formData.my_rating}
                                onChange={(e) => setFormData({...formData, my_rating: Number(e.target.value)})}
                                min="1"
                                max="10"
                                placeholder="Rate from 1 to 10"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="my_review">Review:</label>
                            <textarea
                                id="my_review"
                                value={formData.my_review}
                                onChange={(e) => setFormData({...formData, my_review: e.target.value})}
                                placeholder="Write your review here..."
                                rows="4"
                            />
                        </div>

                        <div className="form-actions">
                            <button type="button" className="cancel-btn" onClick={onClose}>Cancel</button>
                            <button type="submit" className="submit-btn">Add Novel</button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}

export default AddNovelForm;