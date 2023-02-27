import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { BLStatusPage, SignInPage, SignUpPage, HomePage } from "src/routes";
import Layout from "./layout";
import "./App.css";

function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/" element={<Layout />}>
            <Route path="/sign-in" element={<SignInPage />} />
            <Route path="/sign-up" element={<SignUpPage />} />
            <Route path="/blstatus" element={<BLStatusPage />} />
          </Route>
        </Routes>
    </Router>
  );
}

export default App;
