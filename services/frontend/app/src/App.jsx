import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { BLStatusPage, SignInPage, SignUpPage, HomePage, ViewShipmentsPage } from "src/routes";
import { ToastContainer } from "react-toastify";
import Layout from "./layout/Layout";
import ProtectedLayout from "./layout/ProtectedLayout";
import "./App.css";
import StatusPage from "./routes/BLStatus/status";
import ErrorPage from "./routes/BLStatus/error";
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
          <Route path="/view-shipments" element={<ViewShipmentsPage />} />
          <Route path="/blstatus" element={<BLStatusPage />} />
          <Route path="/status" element={<StatusPage />} />
          <Route path="/error" element={<ErrorPage />} />
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
