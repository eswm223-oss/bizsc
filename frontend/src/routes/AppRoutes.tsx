//////////////////////////////////
/*===  URLと画面の対応を管理  ===*/
//////////////////////////////////

import { Route, Routes } from "react-router-dom";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<div>Home</div>} />
    </Routes>
  );
}

export default AppRoutes;
