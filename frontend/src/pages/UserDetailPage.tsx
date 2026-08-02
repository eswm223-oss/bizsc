import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import Card from "../components/Card/Card";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Loading from "../components/Loading/Loading";

import { getUser } from "../api/users";
import type { User } from "../types/user";

function UserDetailPage() {
  const { userId } = useParams();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function featchUser() {
      const id = Number(userId);

      if (!userId || Number.isNaN(id)) {
        setError("ユーザーIDが正しくありません");
        setIsLoading(false);
        return;
      }

      try {
        const response = await getUser(id);
        setUser(response);
      } catch {
        setError("ユーザー情報の取得に失敗しました");
      } finally {
        setIsLoading(false);
      }
    }

    featchUser();
  }, [userId]);

  if (isLoading) {
    return <Loading message="ユーザー情報を読み込んでいます..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!user) {
    return <ErrorMessage message="ユーザー情報が見つかりません" />;
  }

  return (
    <Card title="ユーザー詳細">
      <dl>
        <dt>ID</dt>
        <dd>{user.id}</dd>

        <dt>メールアドレス</dt>
        <dd>{user.email}</dd>

        <dt>ステータス</dt>
        <dd>{user.is_active ? "Active" : "Inactive"}</dd>

        <dt>作成日時</dt>
        <dd>{user.created_at}</dd>

        <dt>更新日時</dt>
        <dd>{user.updated_at}</dd>
      </dl>

      <Link to="/users">ユーザー一覧へ戻る</Link>
    </Card>
  );
}

export default UserDetailPage;
