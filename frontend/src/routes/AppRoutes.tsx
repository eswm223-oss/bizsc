//////////////////////////////////
/*===  URLと画面の対応を管理  ===*/
//////////////////////////////////

import { Route, Routes } from "react-router-dom";
import MainLayout from "../layouts/MainLayout.tsx";
import MainLayoutMantine from "../layouts/MainLayoutMantine.tsx";
import NotFoundPage from "../pages/NotFoundPage";
import HomePageMantine from "../pages/HomePageMantine.tsx";
import UserListPageMantine from "../pages/UserListPageMantine.tsx";
import UserDetailPageMantine from "../pages/UserDetailPageMantine.tsx";
import UserCreatePageMantine from "../pages/UserCreatePageMantine.tsx";
import UserEditPageMantine from "../pages/UserEditPageMantine.tsx";
import MasterList from "../pages/MasterList.tsx";
import TestScreen from "../pages/Test.tsx";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayoutMantine />}>
        <Route path="/" element={<HomePageMantine />} />
        <Route path="/users" element={<UserListPageMantine />} />
        <Route path="/users/new" element={<UserCreatePageMantine />} />
        <Route path="/users/:userId" element={<UserDetailPageMantine />} />
        <Route path="/users/:userId/edit" element={<UserEditPageMantine />} />
      </Route>

      <Route element={<MainLayout />}>
        <Route path="/jquants/master" element={<MasterList />} />
        <Route path="/test" element={<TestScreen />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
