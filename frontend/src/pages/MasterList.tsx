import React, { useEffect, useState } from "react";
import { getMaster } from "../api/jquants";
import type { Master } from "../types/jquants";
import Loading from "../components/Loading/Loading";
import Button from "../components/Button/Button";

const MasterList = () => {
  const [masterList, setMasterList] = useState<Master[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");
  const [page, setPage] = useState(1);
  const [limit] = useState(50);
  const [total, setTotal] = useState(0);

  const fetchMaster = async () => {
    setIsLoading(true);
    const result = await getMaster(search, sortBy, sortOrder, page, limit);
    setMasterList(result.data);
    setIsLoading(false);
  };

  const onClickSearch = (event: React.SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    fetchMaster();
  };

  // if (isLoading) {
  //   return <Loading />;
  // }

  return (
    <>
      <form onSubmit={onClickSearch}>
        <div className="list-page">
          <div className="head">
            <div className="title">Master 一覧</div>
            <div className="seatch-box">
              <div>
                <Button>検索</Button>
              </div>
            </div>
          </div>
        </div>
      </form>
      <div className="list">
        {masterList.map((master) => (
          <div>{master.code}</div>
        ))}
      </div>
    </>
  );
};

export default MasterList;
