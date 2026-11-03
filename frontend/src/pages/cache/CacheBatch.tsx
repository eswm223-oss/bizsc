import { useState, type SubmitEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Card, Stack, Title } from "@mantine/core";
import MgmtForm from "../../components/Form/MgmtForm";
import { runCacheBatch } from "../../api/cache";
import type { CacheRunRequest } from "../../types/cacheMgmt";
import { notifications } from "@mantine/notifications";

function CacheBatch() {
  const navigate = useNavigate();
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [companyCode, setCompanyCode] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  //キャッシュバッチ実行処理
  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!fromDate || !toDate || fromDate > toDate) return;

    const request: CacheRunRequest = {
      fromDate: fromDate,
      toDate: toDate,
      code: companyCode,
      mgmtId: undefined,
    };

    try {
      setIsSubmitting(true);
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
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Stack gap="lg" maw={560}>
      <Title order={2}>キャッシュ処理</Title>
      <Card withBorder padding="lg" radius="md">
        <MgmtForm
          fromDate={fromDate}
          onFromDateChange={setFromDate}
          toDate={toDate}
          onToDateChange={setToDate}
          companyCode={companyCode}
          onCompnayChange={setCompanyCode}
          isSubmitting={isSubmitting}
          submitLabel="キャッシュ作成"
          submittingLabel="作成中..."
          onSubmit={(event) => void handleSubmit(event)}
          onCancel={() => navigate("/jquants/cache")}
        />
      </Card>
    </Stack>
  );
}

export default CacheBatch;
