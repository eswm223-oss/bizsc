//////////////////////////////////
/*===  URLと画面の対応を管理  ===*/
//////////////////////////////////

import { Route, Routes } from "react-router-dom";
import MainLayoutMantine from "../layouts/MainLayoutMantine.tsx";
import NotFoundPage from "../pages/NotFoundPage";
import HomePageMantine from "../pages/HomePageMantine.tsx";
import UserListPageMantine from "../pages/user/UserListPageMantine.tsx";
import UserDetailPageMantine from "../pages/user/UserDetailPageMantine.tsx";
import UserCreatePageMantine from "../pages/user/UserCreatePageMantine.tsx";
import UserEditPageMantine from "../pages/user/UserEditPageMantine.tsx";
import MasterList from "../pages/jquants/MasterList.tsx";

import ValuationList from "../pages/jquants/ValuationList.tsx";
import DailyQuoteList from "../pages/jquants/DailyQuote.tsx";
import SummaryList from "../pages/jquants/SummaryList.tsx";
import CacheMgmtList from "../pages/cache/CacheMgmtList.tsx";
import CacheDetail from "../pages/cache/CacheDetail.tsx";
import CacheBatch from "../pages/cache/CacheBatch.tsx";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayoutMantine />}>
        <Route path="/" element={<HomePageMantine />} />
        <Route path="/users" element={<UserListPageMantine />} />
        <Route path="/users/new" element={<UserCreatePageMantine />} />
        <Route path="/users/:userId" element={<UserDetailPageMantine />} />
        <Route path="/users/:userId/edit" element={<UserEditPageMantine />} />
        <Route path="/jquants/cache" element={<CacheMgmtList />} />
        <Route path="/jquants/cache/detail/" element={<CacheBatch />} />
        <Route path="/jquants/cache/detail/:mgmtId" element={<CacheDetail />} />
        <Route path="/jquants/master" element={<MasterList />} />
        <Route path="/jquants/valuation" element={<ValuationList />} />
        <Route path="/jquants/dailyquote" element={<DailyQuoteList />} />
        <Route path="/jquants/summary" element={<SummaryList />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
