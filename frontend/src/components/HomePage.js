import React from "react";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="homepage">
      <section className="hero-section">
        <h1>Welcome to Skibidi Stories</h1>
        <p className="subtitle">Your AI-powered platform for stories and viral Instagram posts.</p>
        <p>Create amazing stories or Instagram posts!</p>
        <div className="button-group">
          <a href="/create-story" className="btn primary-btn">Create a Story</a>
          <a href="/create-instagram" className="btn secondary-btn">Create Instagram Post</a>
        </div>
      </section>
      <section className="features-section">
        <h2>Why Choose Skibidi Stories?</h2>
        <div className="features">
          <div className="feature">
            <div className="feature-icon">
              <img src="/icons/create.png" alt="Create Icon" />
            </div>
            <h3>Create</h3>
            <p>Unleash your creativity by writing unique stories.</p>
          </div>
          <div className="feature">
            <div className="feature-icon">
              <img src="/icons/explore.png" alt="Explore Icon" />
            </div>
            <h3>Explore</h3>
            <p>Discover stories written by others and get inspired.</p>
          </div>
          <div className="feature">
            <div className="feature-icon">
              <img src="/icons/share.png" alt="Share Icon" />
            </div>
            <h3>Share</h3>
            <p>Share your stories with the world effortlessly.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
