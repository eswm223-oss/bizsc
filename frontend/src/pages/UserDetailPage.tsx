import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import Card from "../components/Card/Card";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Loading from "../components/Loading/Loading";
import Button from "../components/Button/Button";
import Badge from "../components/Badge/Badge";
import { deleteUser, getUser } from "../api/users";

import type { User } from "../types/user";

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}

function UserDetailPage() {
  const { userId } = useParams();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const navigate = useNavigate();

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

    //ユーザ情報取得
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

  async function handleDelete() {
    if (!user) {
      return;
    }

    const shouldDelete = window.confirm(
      "このユーザーを削除してもよろしいですか？",
    );

    if (!shouldDelete) {
      return;
    }

    try {
      setIsDeleting(true);

      await deleteUser(user.id);

      navigate("/users");
    } catch {
      setError("ユーザーの削除に失敗しました。");
    } finally {
      setIsDeleting(false);
    }
  }

  return (
    <div className="row justify-content-center">
      <div className="col-12 col-lg-8 col-xl-6">
        <Card title="ユーザー詳細">
          <dl className="row mb-0">
            <dt className="col-sm-4 mb-3">ID</dt>
            <dd className="col-sm-8 mb-3">{user.id}</dd>

            <dt className="col-sm-4 mb-3">メールアドレス</dt>
            <dd className="col-sm-8 mb-3">{user.email}</dd>

            <dt className="col-sm-4 mb-3">ステータス</dt>
            <dd className="col-sm-8 mb-3">
              <Badge variant={user.is_active ? "success" : "neutral"}>
                {user.is_active ? "有効" : "無効"}
              </Badge>
            </dd>

            <dt className="col-sm-4 mb-3">作成日時</dt>
            <dd className="col-sm-8 mb-3">{formatDateTime(user.created_at)}</dd>

            <dt className="col-sm-4 mb-0">更新日時</dt>
            <dd className="col-sm-8 mb-0">{formatDateTime(user.updated_at)}</dd>
          </dl>

          <div className="d-flex justify-content-between align-items-center mt-4">
            <Link className="btn btn-secondary" to="/users">
              一覧へ戻る
            </Link>

            <div className="d-flex align-items-center gap-2">
              <Link
                className="btn btn-outline-primary"
                to={`/users/${user.id}/edit`}
              >
                編集
              </Link>

              <Button
                type="button"
                variant="danger"
                onClick={handleDelete}
                disabled={isDeleting}
              >
                {isDeleting ? "削除中..." : "削除"}
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default UserDetailPage;
