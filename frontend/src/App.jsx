import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setIsPredicting(false);
    setResult(""); // Clear previous prediction

    if (selectedFile) {
      const previewUrl = URL.createObjectURL(selectedFile);
      setImagePreview(previewUrl);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setIsPredicting(true);

    try {
      const res = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.prediction);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="container">
      <h1>Cat vs Dog Classifier 🐱🐶</h1>
      <p className="accuracy-text">Accuracy: 89%</p>{" "}
      {/* Accuracy Text Below Title */}
      <form onSubmit={handleSubmit} className="form">
        <input
          type="file"
          onChange={handleChange}
          accept="image/*"
          className="file-input"
          style={{ display: "none" }}
          id="fileInput"
        />
        <label htmlFor="fileInput" className="file-label">
          Choose an image
        </label>
        {!result && (
          <button type="submit" className="submit-btn" disabled={isPredicting}>
            {isPredicting ? "Predicting..." : "Predict"}
          </button>
        )}
      </form>
      {imagePreview && (
        <div className="image-preview">
          <img src={imagePreview} alt="Preview" className="preview-img" />
        </div>
      )}
      {result && <h2>Prediction: {result}</h2>}
    </div>
  );
}

export default App;
