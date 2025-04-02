import React from 'react';

function NovelCard({ title, imageUrl, rating, description, status }) {
  return (
    <div className="novel_card">
      <div className="novel-image">
        <img src={imageUrl} alt={title} />
      </div>
      <div className="novel-info">
        <h2 className="novel-title">{title}</h2>
        {description && <p className="novel-description">{description}</p>}
        {rating && <p className="novel-rating">Rating: {rating}</p>}
        {status && <p className="novel-status">Status: {status}</p>}
      </div>
    </div>
  );
}

export default NovelCard;