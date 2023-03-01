import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import { BLStatusPage, SignInPage, SignUpPage, HomePage } from "src/routes";
import Layout from "./layout/Layout";
import ProtectedLayout from "./layout/ProtectedLayout";
import "./App.css";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/" element={<Layout />}>
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/sign-up" element={<SignUpPage />} />
        </Route>
        
        {/* Protected Routes/Routes with SideBar */}
        <Route element={<ProtectedLayout />}>
          <Route path="/blstatus" element={<BLStatusPage />} />
        </Route>
      </Routes>
      <ToastContainer
        position='bottom-right'
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable
        pauseOnHover={false}
        theme='colored'
      />
    </Router>
  );
}

export default App;
