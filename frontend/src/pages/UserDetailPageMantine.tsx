import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Alert,
  Badge,
  Button,
  Card,
  Center,
  Group,
  Loader,
  Modal,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import { deleteUser, getUser } from "../api/users";
import type { User } from "../types/user";

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ja-JP");
}

function UserDetailPageMantine() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteOpened, setDeleteOpened] = useState(false);

  useEffect(() => {
    async function fetchUser() {
      const id = Number(userId);

      if (!userId || Number.isNaN(id)) {
        setError("ユーザーIDが正しくありません");
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const response = await getUser(id);
        setUser(response);
      } catch {
        setError("ユーザー情報の取得に失敗しました");
      } finally {
        setIsLoading(false);
      }
    }

    void fetchUser();
  }, [userId]);

  async function handleDelete() {
    if (!user) {
      return;
    }

    try {
      setIsDeleting(true);
      await deleteUser(user.id);
      navigate("/users");
    } catch {
      setError("ユーザーの削除に失敗しました。");
      setDeleteOpened(false);
    } finally {
      setIsDeleting(false);
    }
  }

  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (error && !user) {
    return (
      <Alert color="red" title="エラー">
        {error}
      </Alert>
    );
  }

  if (!user) {
    return (
      <Alert color="red" title="エラー">
        ユーザー情報が見つかりません
      </Alert>
    );
  }

  return (
    <Stack gap="lg" maw={640}>
      <Title order={2}>ユーザー詳細</Title>

      {error && (
        <Alert color="red" title="エラー">
          {error}
        </Alert>
      )}

      <Card withBorder padding="lg" radius="md">
        <Stack gap="sm">
          <div>
            <Text size="sm" c="dimmed">
              ID
            </Text>
            <Text>{user.id}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              メールアドレス
            </Text>
            <Text>{user.email}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              ステータス
            </Text>
            <Badge color={user.is_active ? "green" : "gray"}>
              {user.is_active ? "有効" : "無効"}
            </Badge>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              作成日時
            </Text>
            <Text>{formatDateTime(user.created_at)}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              更新日時
            </Text>
            <Text>{formatDateTime(user.updated_at)}</Text>
          </div>
        </Stack>
      </Card>

      <Group justify="space-between">
        <Button component={Link} to="/users" variant="default">
          一覧へ戻る
        </Button>
        <Group>
          <Button
            component={Link}
            to={`/users/${user.id}/edit`}
            variant="light"
          >
            編集
          </Button>
          <Button color="red" onClick={() => setDeleteOpened(true)}>
            削除
          </Button>
        </Group>
      </Group>

      <Modal
        opened={deleteOpened}
        onClose={() => setDeleteOpened(false)}
        title="ユーザーの削除"
        centered
      >
        <Text mb="md">このユーザーを削除してもよろしいですか？</Text>
        <Group justify="flex-end">
          <Button
            variant="default"
            onClick={() => setDeleteOpened(false)}
            disabled={isDeleting}
          >
            キャンセル
          </Button>
          <Button color="red" loading={isDeleting} onClick={() => void handleDelete()}>
            削除する
          </Button>
        </Group>
      </Modal>
    </Stack>
  );
}

export default UserDetailPageMantine;
