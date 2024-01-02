
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Album from "./Album";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Album />} />
        
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
