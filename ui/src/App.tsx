import React from "react";
import { Routes, Route, Outlet, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SettingPage from "./pages/SettingPage";
import VideoDetailPage from "./pages/VideoDetailPage";

function App() {
    return (
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/videos/:id" element={<VideoDetailPage />} />
            <Route path="/settings" element={<SettingPage />} />
        </Routes>
    );
}

export default App;
