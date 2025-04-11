import React, { useState } from "react";
import axios from "axios";
import "./CreateStory.css";

function CreateStory() {
  const [description, setDescription] = useState("");
  const [storyType, setStoryType] = useState("Bedtime");
  const [moral, setMoral] = useState("");
  const [generatedStory, setGeneratedStory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const uniqueId = `story_${Date.now()}_${Math.random().toString(36).substring(2, 10)}`;

    try {
      console.log("Sending request with unique ID:", uniqueId);
      const response = await axios.post("http://127.0.0.1:5000/generate_story", {
        description,
        storyType,
        moral,
        id: uniqueId,
      });

      setGeneratedStory({ ...response.data, uniqueId });
    } catch (error) {
      console.error("Error generating story:", error);
      alert("Failed to generate story. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveStory = async () => {
    try {
      await axios.post("http://localhost:5000/save_story", {
        user_id: 1,
        title: generatedStory.title,
        description,
        content: generatedStory.pages.map((page) => page.text).join(". "),
        id: generatedStory.id,
        illustrations: generatedStory.pages.map((page) => page.image),
        audio_url: generatedStory.audio_url || "",
      });

      alert("Story saved successfully!");
      setIsSaved(true);
    } catch (error) {
      console.error("Error saving story:", error);
      alert("Failed to save story. Please try again.");
    }
  };

  return (
    <div className="create-story">
      <h1>Create Your Story</h1>
      <form onSubmit={handleSubmit} className="create-story-form">
        <label>
          Story Type:
          <select
            value={storyType}
            onChange={(e) => setStoryType(e.target.value)}
            className="form-select"
          >
            <option value="Bedtime">Bedtime Story</option>
            <option value="Educational">Educational Story</option>
          </select>
        </label>
        <label>
          Description:
          <textarea
            placeholder="Write a short description of your story..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="form-textarea"
          />
        </label>
        <label>
          Moral (Optional):
          <select
            value={moral}
            onChange={(e) => setMoral(e.target.value)}
            className="form-select"
          >
            <option value="">None</option>
            <option value="Helping others makes you stronger">
              Helping others makes you stronger
            </option>
            <option value="Bravery leads to rewards">
              Bravery leads to rewards
            </option>
            <option value="Honesty is the best policy">
              Honesty is the best policy
            </option>
          </select>
        </label>
        <button type="submit" className="btn-create">
          {loading ? "Creating..." : "Create"}
        </button>
      </form>

      {generatedStory && (
        <div className="generated-story">
          <h2>{generatedStory.title}</h2>
          <div className="story-content">
            <p>{generatedStory.content}</p>
          </div>
          {!isSaved && (
            <button onClick={handleSaveStory} className="btn-save">
              Save Story
            </button>
          )}
          {isSaved && (
            <p style={{ color: "green" }}>Story has been saved successfully!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default CreateStory;
