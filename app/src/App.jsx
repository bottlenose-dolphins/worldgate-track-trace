import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { SignInPage, SignUpPage, HomePage } from "src/routes";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sign-in" element={<SignInPage />} />
        <Route path="/sign-up" element={<SignUpPage/>} />

      </Routes>
    </Router>
  );
}

export default App;
