import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { SignInPage } from "src/routes";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignInPage />} />
        <Route path="/sign-in" element={<SignInPage />} />
      </Routes>
    </Router>
  );
}

export default App;
