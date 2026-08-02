//////////////////////////////////
/*===  URLと画面の対応を管理  ===*/
//////////////////////////////////

import { Route, Routes } from "react-router-dom";
import MainLayout from "../layouts/MainLayout.tsx";
import NotFoundPage from "../pages/NotFoundPage";
import HomePage from "../pages/HomePage.tsx";
import UserListPage from "../pages/UserListPage.tsx";
import UserDetailPage from "../pages/UserDetailPage.tsx";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/users" element={<UserListPage />} />
        <Route path="/users/:userId" element={<UserDetailPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
