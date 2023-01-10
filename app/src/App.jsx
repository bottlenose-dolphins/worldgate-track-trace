import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from './components/Navbar';
import { SignInPage } from "src/routes";
import "./App.css";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<SignInPage />} />
        <Route path="/sign-in" element={<SignInPage />} />
        <Route path="/home" element={<SignInPage />} />
        <Route path="/worldgate" element={<SignInPage />} />
        <Route path="/about" element={<SignInPage />} />


      </Routes>
    </Router>
  );
}

export default App;
