import React from 'react';
import NovelCard from './NovelCard';

function NovelGrid({ novels }) {
  return (
    <div className="novels-grid">
      {novels.map((novel) => (
        <NovelCard 
          key={novel.id}
          title={novel.title}
          imageUrl={novel.image_url}
          rating={novel.my_rating}
        />
      ))}
    </div>
  );
}

export default NovelGrid;