import { useState } from "react";
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
import { notifications } from "@mantine/notifications";
import type {
  CacheMgmtRecord,
  CacheRunRequest,
  CacheStatus,
} from "../../types/cacheMgmt";
import {
  deleteCacheMgmt,
  getCacheMgmtById,
  runCacheBatch,
} from "../../api/cache";
import { useQuery } from "@tanstack/react-query";

function CacheDetail() {
  const { mgmtId } = useParams();
  const navigate = useNavigate();
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteOpened, setDeleteOpened] = useState(false);

  function formatDateTime(value: string) {
    if (!value) return "";
    return new Date(value).toLocaleString("ja-JP");
  }

  // ステータス
  function getBadgeColor(status: CacheStatus | null) {
    switch (status) {
      case "Complete":
        return "lime.6";
      case "Waiting":
        return "orange";
      case "Running":
        return "cyan.6";
      case "Error":
        return "red.9";
      default:
        return "gray";
    }
  }

  // fetch管理
  const {
    data: response,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["mgmt", mgmtId],
    queryFn: () => fetchData(),
  });

  // fetch処理
  const fetchData = async () => {
    if (!mgmtId) return {} as CacheMgmtRecord;
    const result = await getCacheMgmtById(mgmtId);
    return result;
  };
  // fetch後アサイン
  const data: CacheMgmtRecord = response ?? ({} as CacheMgmtRecord);

  // delete処理
  const handleDelete = async () => {
    if (!mgmtId) return;
    try {
      setIsDeleting(true);
      await deleteCacheMgmt(mgmtId);
      notifications.show({
        title: "削除完了",
        message: "データを削除しました。",
        color: "green",
        autoClose: 3000,
      });

      navigate("/jquants/cache");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "不明なエラーが発生しました";

      notifications.show({
        title: "削除エラー",
        message: errorMessage,
        color: "red",
        autoClose: 5000,
      });
    } finally {
      setIsDeleting(false);
    }
  };

  //キャッシュバッチ実行処理
  async function handleSubmit() {
    const request: CacheRunRequest = {
      fromDate: data.from_date.toString(),
      toDate: data.to_date.toString(),
      code: data.company_code || undefined,
      mgmtId: data.id,
    };

    try {
      const result = await runCacheBatch(request);
      notifications.show({
        title: "キャッシュバッチ起動",
        message: `message:${result?.message}(${result?.mgmtId})`,
        color: "cyan.6",
        autoClose: 5000,
      });
      navigate("/jquants/cache");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "不明なエラーが発生しました";
      notifications.show({
        title: "実行エラー",
        message: errorMessage,
        color: "red",
        autoClose: 5000,
      });
    }
  }

  // ローディング
  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }
  // 取得エラー
  if (error || !response) {
    return (
      <Alert color="red" title="取得エラー">
        {error?.message ?? "データが見つかりません"}
      </Alert>
    );
  }
  return (
    <Stack gap="lg" maw={640}>
      <Title order={2}>キャッシュ処理操作</Title>
      <Card withBorder padding="lg" radius="md">
        <Stack gap="sm">
          <div>
            <Text size="sm" c="dimmed">
              ID
            </Text>
            <Text>{data.id}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              対象日From
            </Text>
            <Text>{data.from_date}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              対象日To
            </Text>
            <Text>{data.to_date}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              企業コード
            </Text>
            <Text>{data.company_code}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              ステータス（上場銘柄）
            </Text>
            <Badge color={getBadgeColor(data.status_master)}>
              {data.status_master}
            </Badge>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              ステータス（株価四本値）
            </Text>
            <Badge color={getBadgeColor(data.status_dailyBar)}>
              {data.status_dailyBar}
            </Badge>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              ステータス（バリュエーション指標）
            </Text>
            <Badge color={getBadgeColor(data.status_valuation)}>
              {data.status_valuation}
            </Badge>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              ステータス（財務情報）
            </Text>
            <Badge color={getBadgeColor(data.status_summary)}>
              {data.status_summary}
            </Badge>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              備考
            </Text>
            <Text>{data.remarks}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed">
              更新日時
            </Text>
            <Text>{formatDateTime(data.updated_at?.toString())}</Text>
          </div>
        </Stack>
      </Card>

      <Group justify="space-between">
        <Button component={Link} to="/jquants/cache" variant="default">
          一覧へ戻る
        </Button>
        <Group>
          <Button
            variant="light"
            onClick={() => handleSubmit()}
            disabled={
              data.status_master == "Running" ||
              data.status_dailyBar == "Running" ||
              data.status_valuation == "Running" ||
              data.status_summary == "Running" ||
              (data.status_master == "Complete" &&
                data.status_dailyBar == "Complete" &&
                data.status_valuation == "Complete" &&
                data.status_summary == "Complete")
            }
          >
            キャッシュ開始
          </Button>
          <Button color="red" onClick={() => setDeleteOpened(true)}>
            削除
          </Button>
        </Group>
      </Group>

      <Modal
        opened={deleteOpened}
        onClose={() => setDeleteOpened(false)}
        title="キャッシュの詳細を削除"
        centered
      >
        <Text mb="md">このキャッシュの詳細を削除してもよろしいですか？</Text>
        <Group justify="flex-end">
          <Button
            variant="default"
            onClick={() => setDeleteOpened(false)}
            disabled={isDeleting}
          >
            キャンセル
          </Button>
          <Button
            color="red"
            loading={isDeleting}
            onClick={() => void handleDelete()}
            disabled={!mgmtId || isDeleting}
          >
            削除する
          </Button>
        </Group>
      </Modal>
    </Stack>
  );
}

export default CacheDetail;
