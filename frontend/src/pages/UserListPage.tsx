import { useEffect, useState } from "react";
import { getUsers } from "../api/users";
import type { User } from "../types/user";
import { Link } from "react-router-dom";

import Card from "../components/Card/Card";
import Loading from "../components/Loading/Loading";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Badge from "../components/Badge/Badge";

import "./UserListPage.css";

function UserListPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [activeFilter, setActiveFilter] = useState("");

  //*************************************** */
  //screen処理
  //*************************************** */
  function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    const isActive = activeFilter === "" ? undefined : activeFilter === "true";
    fetchUsers(search, isActive);
  }

  async function fetchUsers(searchValue?: string, isActiveValue?: boolean) {
    try {
      setIsLoading(true);
      setError(null);

      const response = await getUsers(searchValue, isActiveValue);
      setUsers(response.users);
    } catch {
      setError("ユーザー一覧の取得に失敗しました");
    } finally {
      setIsLoading(false);
    }
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

          <button type="submit">検索</button>
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
      </Card>
    </div>
  );
}

export default UserListPage;
