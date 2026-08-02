import { useEffect, useState } from "react";
import { getUsers } from "../api/users";
import type { User } from "../types/user";
import { Link } from "react-router-dom";

import Card from "../components/Card/Card";
import Loading from "../components/Loading/Loading";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";

import "./UserListPage.css";

function UserListPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchUsers() {
      try {
        const response = await getUsers();
        setUsers(response.users);
      } catch {
        setError("ユーザー一覧の取得に失敗しました");
      } finally {
        setIsLoading(false);
      }
    }

    fetchUsers();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div className="user-list-page">
      <Card title="Users">
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
                  <td className="user-status">
                    {user.is_active ? "Active" : "Inactive"}
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
