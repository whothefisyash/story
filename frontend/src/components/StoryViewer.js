// D:\Ahh\Projects\story\frontend\src\components\StoryViewer.js

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import HTMLFlipBook from "react-pageflip"; // Import react-pageflip
import "./StoryViewer.css";

function StoryViewer() {
  const { id } = useParams(); // Get story ID from URL params
  const [story, setStory] = useState(null);
  
  const [audioUrl, setAudioUrl] = useState(null);
  const [audio, setAudio] = useState(null); // Audio object
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false); // Pause state
  const [speed, setSpeed] = useState(1); // Default playback speed

  const [quizQuestions, setQuizQuestions] = useState([]);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [results, setResults] = useState(null); // To store quiz results

  useEffect(() => {
    const fetchStory = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/story/${id}`);
        console.log("API Response:", response.data); // Log full API response
        setStory(response.data);
      } catch (error) {
        console.error("Error fetching story:", error);
      }
    };
    fetchStory();
  }, [id]);
  
  


  const handleAnswerSelect = (questionIndex, selectedOption) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionIndex]: selectedOption,
    }));
  };

  const handleSubmitQuiz = () => {
    const resultsData = quizQuestions.map((question, index) => ({
      question: question.question,
      selectedAnswer: selectedAnswers[index],
      correctAnswer: question.answer,
      isCorrect: selectedAnswers[index] === question.answer,
    }));
    setResults(resultsData);
  };


  const handleGenerateAudio = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/generate_tts",
        { text: story.content }
      );
      const audioUrlFromServer = `http://127.0.0.1:5000/generated_audio/story_audio.mp3`;
      setAudioUrl(audioUrlFromServer);
  
      // Create a new Audio object with the new URL
      const newAudio = new Audio(audioUrlFromServer);
      newAudio.playbackRate = speed;
      setAudio(newAudio);
  
      alert("Audio generated successfully!");
    } catch (error) {
      console.error("Error generating TTS:", error);
      alert("Failed to generate audio. Please try again.");
    }
  };
  
  
  const handlePlayAudio = () => {
    if (audio) {
      if (isPaused) {
        audio.play(); // Resume playback
        setIsPaused(false);
      } else {
        audio.play(); // Start playback
      }
      setIsPlaying(true);
    }
  };

  const handlePauseAudio = () => {
    if (audio) {
      audio.pause();
      setIsPlaying(false);
      setIsPaused(true); // Set pause state
    }
  };

  const handleStopAudio = () => {
    if (audio) {
      audio.pause();
      audio.currentTime = 0; // Reset playback to the beginning
      setIsPlaying(false);
      setIsPaused(false); // Reset pause state
    }
  };

  const handleSpeedChange = (newSpeed) => {
    if (audio) {
      audio.playbackRate = newSpeed;
    }
    setSpeed(newSpeed);
  };

  if (!story) return <div>Loading...</div>;

  
  const sentences = story.content.split(". ");
  const pages = sentences.map((text, index) => ({
    text: text,
    image_url: story.illustration_urls[index] || "placeholder.png", // Use placeholder if no image exists
  }));
  // const pages = story.pages || [];

  return (
    <div className="story-viewer">
      <h1>{story.title}</h1>

      <HTMLFlipBook width={400} height={500} className="storybook">
        {(story.pages || []).map((page, index) => { // Safely handle undefined pages
          const imageUrl = page.image 
            ? `http://127.0.0.1:5000${page.image}`
            : "http://127.0.0.1:5000/static/placeholder.png";

          console.log(`Rendering page ${index + 1}:`, imageUrl); // Debug log

          return (
            <div key={index} className="storybook-page">
              <div className="left-page">
                <img 
                  src={imageUrl} 
                  alt={`Page ${index + 1}`}
                  onError={(e) => {
                    console.error("Failed to load image:", imageUrl);
                    e.target.onerror = null;
                    e.target.src = "http://127.0.0.1:5000/static/placeholder.png";
                  }}
                />
              </div>
              <div className="right-page">
                <p>{page.text || "Page content missing"}</p>
              </div>
            </div>
          );
        })}
      </HTMLFlipBook>






      {/* TTS Controls */}
      <div className="tts-controls">
        {!audioUrl && (
          <button onClick={handleGenerateAudio}>Generate Audio</button>
        )}
        {audioUrl && (
          <>
            <button onClick={handlePlayAudio} disabled={isPlaying}>Play</button>
            <button onClick={handlePauseAudio} disabled={!isPlaying || isPaused}>Pause</button>
            <button onClick={handleStopAudio}>Stop</button>
            <label>
              Speed:
              <select value={speed} onChange={(e) => handleSpeedChange(Number(e.target.value))}>
                <option value="0.5">0.5x</option>
                <option value="1">1x</option>
                <option value="1.5">1.5x</option>
                <option value="2">2x</option>
              </select>
            </label>
            <a href={audioUrl} download="story_audio.mp3" className="download-btn">Download Audio</a>
          </>
        )}
      </div>

      {/* Interactive Quiz Section */}
      <div className="quiz-section">
        <h2>Interactive Quiz</h2>
        {quizQuestions.map((question, index) => (
          <div key={index} className="quiz-question">
            <p>{question.question}</p>
            {question.options.map((option) => (
              <button
                key={option}
                onClick={() => handleAnswerSelect(index, option)}
                className={selectedAnswers[index] === option ? "selected" : ""}
              >
                {option}
              </button>
            ))}
          </div>
        ))}
        
        {quizQuestions.length > 0 && (
          <button onClick={handleSubmitQuiz} className="submit-quiz-btn">Submit Quiz</button>
        )}

        {/* Display Results */}
        {results && (
          <div className="quiz-results">
            <h3>Quiz Results:</h3>
            {results.map((result, index) => (
              <p key={index}>
                Q: {result.question} <br />
                Your Answer: {result.selectedAnswer} <br />
                Correct Answer: {result.correctAnswer} <br />
                Result: {result.isCorrect ? "Correct ✅" : "Wrong ❌"}
              </p>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}

export default StoryViewer;
