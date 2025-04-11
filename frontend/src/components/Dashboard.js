// D:\Ahh\Projects\story\frontend\src\components\Dashboard.js

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom"; // Import useLocation
import { Link } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const [stories, setStories] = useState([]);
  const location = useLocation(); // Get current route

  useEffect(() => {
    const fetchStories = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_stories?user_id=1");
        setStories(response.data);
      } catch (error) {
        console.error("Error fetching stories:", error);
      }
    };

    fetchStories();
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>{location.pathname === "/dashboard" ? "My Stories" : "Explore Stories"}</h1> {/* Dynamic heading */}
      </header>

      <div className="story-grid">
        {stories.map((story) => (
          <div key={story.id} className="story-card">
            <img 
              src={`http://127.0.0.1:5000${story.illustration_urls[0]}`} 
              alt={story.title} 
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "http://127.0.0.1:5000/static/placeholder.png";
              }} 
            />
            <h3>{story.title}</h3>
            <Link to={`/story/${story.id}`} className="read-now">Read Now</Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
 