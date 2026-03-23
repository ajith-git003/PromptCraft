import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import { ThemeProvider } from "./context/ThemeContext";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <ThemeProvider>
      <div>
        <Navbar onToggleSidebar={() => setSidebarOpen((o) => !o)} />
        <Home sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
      </div>
    </ThemeProvider>
  );
}

export default App;
