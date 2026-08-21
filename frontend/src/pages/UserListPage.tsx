import { useEffect, useState } from "react";
import { getUsers } from "../api/users";
import type { User } from "../types/user";
import { Link } from "react-router-dom";

import Card from "../components/Card/Card";
import Loading from "../components/Loading/Loading";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Badge from "../components/Badge/Badge";
import Button from "../components/Button/Button";

import "./UserListPage.css";

function UserListPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [activeFilter, setActiveFilter] = useState("");
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [total, setTotal] = useState(0);
  const totalPages = Math.max(1, Math.ceil(total / limit)); //ceil←小数点切り上げ

  //*************************************** */
  //screen処理
  //*************************************** */

  //検索ボタン処理
  function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
    //submitでも画面を再読み込みさせないようにする
    event.preventDefault();

    //検索
    const isActive = activeFilter === "" ? undefined : activeFilter === "true";
    setPage(1);
    fetchUsers(search, isActive, sortBy, sortOrder, 1, limit);
  }

  //検索処理
  async function fetchUsers(
    searchValue?: string,
    isActiveValue?: boolean,
    sortByValue?: string,
    sortOrderValue?: string,
    pageValue?: number,
    limitValue?: number,
  ) {
    try {
      setIsLoading(true);
      setError(null);

      const response = await getUsers(
        searchValue,
        isActiveValue,
        sortByValue,
        sortOrderValue,
        pageValue,
        limitValue,
      );
      setUsers(response.users);
      setTotal(response.total);
    } catch {
      setError("ユーザー一覧の取得に失敗しました");
    } finally {
      setIsLoading(false);
    }
  }

  //ページネーション(前)
  function handlePreviousPage() {
    if (page <= 1) {
      return;
    }

    const previousPage = page - 1;
    const isActive = activeFilter === "" ? undefined : activeFilter === "true";

    setPage(previousPage);

    fetchUsers(search, isActive, sortBy, sortOrder, previousPage, limit);
  }

  //ページネーション(次)
  function handleNextPage() {
    if (page >= totalPages) {
      return;
    }

    const previousPage = page + 1;
    const isActive = activeFilter === "" ? undefined : activeFilter === "true";

    setPage(previousPage);

    fetchUsers(search, isActive, sortBy, sortOrder, previousPage, limit);
  }

  //*************************************** */
  //preparation
  //*************************************** */
  useEffect(() => {
    let ignore = false;

    async function loadUsers() {
      try {
        const response = await getUsers();

        if (!ignore) {
          setUsers(response.users);
          setTotal(response.total);
        }
      } catch {
        if (!ignore) {
          setError("ユーザー一覧の取得に失敗しました");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    loadUsers();

    return () => {
      ignore = true;
    };
  }, []);

  //*************************************** */
  //return処理
  //*************************************** */
  if (isLoading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div className="user-list-page">
      <Card title="ユーザー一覧">
        <form onSubmit={handleSearch} className="user-search-form">
          <input
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="メールアドレスで検索"
          />

          <select
            value={activeFilter}
            onChange={(event) => setActiveFilter(event.target.value)}
          >
            <option value="">全て</option>
            <option value="true">有効</option>
            <option value="false">無効</option>
          </select>

          <select
            value={sortBy}
            onChange={(event) => setSortBy(event.target.value)}
          >
            <option value="id">ID</option>
            <option value="email">メールアドレス</option>
            <option value="created_at">作成日時</option>
            <option value="updated_at">更新日時</option>
          </select>

          <select
            value={sortOrder}
            onChange={(event) => setSortOrder(event.target.value)}
          >
            <option value="asc">昇順</option>
            <option value="desc">降順</option>
          </select>

          <Button type="submit">検索</Button>
        </form>
        <div className="user-list-actions">
          <Link to="/users/new">ユーザーを新規作成</Link>
        </div>
        {users.length === 0 ? (
          <p className="user-list-empty">ユーザーが登録されていません</p>
        ) : (
          <table className="user-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>メールアドレス</th>
                <th>ステータス</th>
                <th>操作</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.email}</td>
                  <td>
                    <Badge variant={user.is_active ? "success" : "neutral"}>
                      {user.is_active ? "有効" : "無効"}
                    </Badge>
                  </td>
                  <td>
                    <Link to={`/users/${user.id}`}>詳細</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <div className="user-pagination">
          <button
            type="button"
            onClick={handlePreviousPage}
            disabled={page <= 1}
          >
            前へ
          </button>
          <span>
            {page} / {totalPages}
          </span>
          <button
            type="button"
            onClick={handleNextPage}
            disabled={page >= totalPages}
          >
            次へ
          </button>
        </div>
      </Card>
    </div>
  );
}

export default UserListPage;
