import { Outlet } from "react-router-dom";
import Footer from "../components/Footer";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import "./MainLayout.css";

function MainLayout() {
  return (
    <div className="main-layout">
      <Header />

      <div className="main-layout__body">
        <Sidebar />

        <main className="main-layout__content">
          <div className="container-fluid">
            <Outlet />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}

export default MainLayout;
