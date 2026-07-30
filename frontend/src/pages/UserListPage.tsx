import { useEffect, useState } from "react";
import { getUsers } from "../api/users";
import type { User } from "../types/user";

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
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>Users</h1>

      {users.length === 0 ? (
        <p>ユーザーが登録されていません</p>
      ) : (
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {user.email} / {user.is_active ? "Active" : "Inactive"}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default UserListPage;
