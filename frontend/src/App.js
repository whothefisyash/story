import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import StoryViewer from "./components/StoryViewer";
import CreateStory from "./components/CreateStory";
import HomePage from "./components/HomePage";
import ContactPage from "./components/ContactPage";
import InstagramGenerator from './components/InstagramGenerator';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/story/:id" element={<StoryViewer />} />
        <Route path="/create-story" element={<CreateStory />} />
        <Route path="/contact-us" element={<ContactPage />} />
        <Route path="/create-instagram" element={<InstagramGenerator />} />
      </Routes>
    </Router>
  );
}

export default App;
