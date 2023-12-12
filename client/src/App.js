import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RetrievePage from './components/retrieve/RetrievePage';
import HomePage from './components/homepage/HomePage';

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/retrieve" element={<RetrievePage/>} />
        </Routes>
      </Router>
  );
}
export default App;