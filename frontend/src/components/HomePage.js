import React from "react";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="homepage">
      <div className="hero-section">
        <h1>Welcome to Skibidi Stories</h1>
        <p>Create amazing stories or INstagram posts!</p>
        <div className="button-group">
          <a href="/create-story" className="btn primary-btn">Create a Story</a>
          <a href="/create-instagram" className="btn secondary-btn">Create Instagram Post</a>
        </div>
      </div>
      <div className="features-section">
        <h2>Why Choose Skibidi Stories?</h2>
        <div className="features">
          <div className="feature">
            <img src="/icons/create.png" alt="Create Icon" />
            <h3>Create</h3>
            <p>Unleash your creativity by writing unique stories.</p>
          </div>
          <div className="feature">
            <img src="/icons/explore.png" alt="Explore Icon" />
            <h3>Explore</h3>
            <p>Discover stories written by others and get inspired.</p>
          </div>
          <div className="feature">
            <img src="/icons/share.png" alt="Share Icon" />
            <h3>Share</h3>
            <p>Share your stories with the world effortlessly.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
