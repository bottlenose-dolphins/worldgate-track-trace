import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { BLStatusPage, SignInPage, SignUpPage, HomePage } from "src/routes";
import Layout from "./layout";
import "./App.css";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/sign-up" element={<SignUpPage />} />
          <Route path="/blstatus" element={<BLStatusPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
