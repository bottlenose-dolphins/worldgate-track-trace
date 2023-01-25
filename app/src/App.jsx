import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { BLStatusPage, SignInPage, SignUpPage } from "src/routes";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignInPage />} />
        <Route path="/sign-in" element={<SignInPage />} />
        <Route path="/sign-up" element={<SignUpPage/>} />
        <Route path="/blstatus" element={<BLStatusPage/>} />
      </Routes>
    </Router>
  );
}

export default App;
