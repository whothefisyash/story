import React, { useState } from 'react';
import axios from 'axios';
import './InstagramGenerator.css';

function InstagramGenerator() {
  const [inputText, setInputText] = useState('');
  const [generatedPost, setGeneratedPost] = useState(null);
  const [loading, setLoading] = useState(false);
  const [instagramUserId, setInstagramUserId] = useState('');
  const [accessToken, setAccessToken] = useState('');

  const handleGenerate = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5000/generate-instagram",
        { text: inputText }
      );
      setGeneratedPost(response.data);
    } catch (error) {
      alert(error.response?.data?.error || "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handlePostToInstagram = async () => {
    if (!instagramUserId || !accessToken) {
      alert("Please provide Instagram User ID and Access Token");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5000/post-to-instagram",
        {
          ig_user_id: instagramUserId,
          access_token: accessToken,
          image_url: generatedPost.image_url,
          caption: `${generatedPost.caption}\n${generatedPost.hashtags}`
        }
      );
      alert(response.data.message || "Posted to Instagram successfully!");
    } catch (error) {
      alert(error.response?.data?.error || "Failed to post to Instagram");
    }
  };

  const handleCopyText = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => alert('Copied to clipboard!'))
      .catch(() => alert('Copy failed'));
  };

  return (
    <div className="instagram-generator">
      <h2>Create Instagram Post</h2>

      {/* Credential Inputs */}
      <div className="credential-inputs">
        <input
          type="text"
          placeholder="Instagram User ID"
          value={instagramUserId}
          onChange={(e) => setInstagramUserId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Instagram Access Token"
          value={accessToken}
          onChange={(e) => setAccessToken(e.target.value)}
        />
      </div>

      {/* Help Text */}
      <div className="credential-help">
        <p>
          Don't know how to get these?{' '}
          <a href="https://developers.facebook.com/docs/instagram-api/getting-started" 
             target="_blank" 
             rel="noopener noreferrer">
            Learn here
          </a>
        </p>
      </div>

      {/* Input Section */}
      <div className="input-section">
        <textarea
          placeholder="Describe your post (e.g., 'Morning coffee vibes')"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button onClick={handleGenerate} disabled={!inputText || loading}>
          {loading ? 'Generating...' : 'Generate Post'}
        </button>
      </div>

      {/* Generated Post Preview */}
      {generatedPost && (
        <div className="post-preview">
          {/* Image Section */}
          <div className="image-section">
            <h3>Your Instagram Image</h3>
            <img src={generatedPost.image_url} alt="Generated post" />
            <div className="image-actions">
              <a 
                href={generatedPost.image_url} 
                download="instagram_post.jpg"
                className="btn download-btn"
              >
                Download Image
              </a>
              <button 
                className="btn post-btn"
                onClick={handlePostToInstagram}
              >
                Post to Instagram
              </button>
            </div>
          </div>

          {/* Text Content */}
          <div className="text-content">
            <div className="caption-section">
              <h3>Caption</h3>
              <div className="text-box">
                <p>{generatedPost.caption}</p>
                <button 
                  className="copy-btn"
                  onClick={() => handleCopyText(generatedPost.caption)}
                >
                  📋 Copy
                </button>
              </div>
            </div>

            <div className="hashtags-section">
              <h3>Hashtags</h3>
              <div className="text-box">
                <p>{generatedPost.hashtags}</p>
                <button
                  className="copy-btn"
                  onClick={() => handleCopyText(generatedPost.hashtags)}
                >
                  📋 Copy
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default InstagramGenerator;
