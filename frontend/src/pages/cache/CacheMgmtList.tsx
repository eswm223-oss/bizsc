import React, { useState } from "react";
import { getCacheMgmt } from "../../api/cache";
import type { CacheMgmtRecord, SearchRequest } from "../../types/cahceMgmt";
import { useQuery } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  Group,
  LoadingOverlay,
  Pagination,
  Stack,
  Table,
  Text,
  TextInput,
  Title,
  ScrollArea,
  Box,
  Grid,
  Badge,
  Flex,
} from "@mantine/core";
import classes from "../TableScrollArea.module.css";
import { DatePresetsInput } from "../../components/Input/DatePresetsInput";
import { useNavigate } from "react-router-dom";

const CacheMgmtList = () => {
  const [searchRequest, setSearchRequest] = useState<SearchRequest>({
    keyword: undefined,
    date: null,
  });
  const navigate = useNavigate();
  const [searchAppliedRequest, setSearchAppliedRequest] =
    useState<SearchRequest>({ keyword: undefined, date: null });
  const [sortBy] = useState("id");
  const [sortOrder] = useState("asc");
  const [page, setPage] = useState(1);
  const [limit] = useState(50);
  const [scrolled, setScrolled] = useState(false);

  function formatDateTime(value: string) {
    if (!value) return "";
    return new Date(value).toLocaleString("ja-JP");
  }

  // ステータス
  function getBadgeColor(
    status: "Complete" | "Waiting" | "Running" | "Error" | undefined,
  ) {
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

  //「検索」ボタン処理
  const handleSearch = (event: React.SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    setPage(1);
    setSearchAppliedRequest(searchRequest);
  };

  //「リセット」ボタン処理
  const handleReset = () => {
    const resetRequest = {
      keyword: "",
      date: null,
    };
    setPage(1);
    setSearchRequest(resetRequest);
    setSearchAppliedRequest(resetRequest);
  };

  // ページネーション処理
  const handlePageChange = (nextPage: number) => {
    setPage(nextPage);
  };

  // fetch管理
  const {
    data: response,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["master", searchAppliedRequest, sortBy, sortBy, page],
    queryFn: () => fetchData(),
  });

  // fetch処理
  const fetchData = async () => {
    const result = await getCacheMgmt(
      searchAppliedRequest.keyword,
      searchAppliedRequest.date,
      sortBy,
      sortOrder,
      page,
      limit,
    );
    return result;
  };

  // fetch後アサイン
  const data: CacheMgmtRecord[] = response?.data ?? [];
  const total = response?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));
  // リストデータ
  console.log(data[0]);
  const rows = data.map((row) => (
    <Table.Tr key={row.id}>
      <Table.Td>
        <Text
          c="blue"
          td="underline"
          style={{ cursor: "pointer" }}
          onClick={() => navigate(`/jquants/cache/detail/${row.id}`)}
        >
          {row.id}
        </Text>
      </Table.Td>
      <Table.Td>{row.from_date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.from_date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.company_code}</Table.Td>
      <Table.Td>
        <Badge color={getBadgeColor(row.status_master)}>
          {row.status_master}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Badge color={getBadgeColor(row.status_dailyBar)}>
          {row.status_dailyBar}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Badge color={getBadgeColor(row.status_valuation)}>
          {row.status_valuation}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Badge color={getBadgeColor(row.status_summary)}>
          {row.status_summary}
        </Badge>
      </Table.Td>
      <Table.Td>{row.remarks}</Table.Td>
      <Table.Td>{formatDateTime(row.updated_at?.toString())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Stack gap="lg">
      <div>
        <Title order={2}>キャッシュ処理実行一覧</Title>

        <Grid>
          <Grid.Col span={6}>
            <Flex justify="flex-start">
              <Text c="dimmed" size="sm" mt={4}>
                {total} 件
              </Text>
            </Flex>
          </Grid.Col>

          <Grid.Col span={6}>
            <Flex justify="flex-end">
              <Button
                mt={4}
                onClick={() => {
                  navigate("/jquants/cache/detail");
                }}
              >
                キャッシュ開始
              </Button>
            </Flex>
          </Grid.Col>
        </Grid>
      </div>

      <Card withBorder padding="md" radius="md">
        <form onSubmit={handleSearch}>
          <Grid>
            <Grid.Col span={{ base: 12, md: 5, lg: 3 }} align="flex-end">
              <TextInput
                label="銘柄キーワード"
                placeholder="銘柄キーワードで検索"
                value={searchRequest.keyword}
                onChange={(event) => {
                  const value = event.currentTarget.value;
                  setSearchRequest((prev) => ({
                    ...prev,
                    keyword: value,
                  }));
                }}
                style={{ flex: "1 1 220px" }}
              />
            </Grid.Col>
            <Grid.Col span={{ base: 12, md: 5, lg: 3 }} align="flex-end">
              <DatePresetsInput
                value={searchRequest.date}
                onChange={(date) => {
                  setSearchRequest((prev) => ({
                    ...prev,
                    date,
                  }));
                }}
                label={"情報適用年月日"}
              />
            </Grid.Col>
            <Grid.Col span={{ base: 12, md: 5, lg: 3 }} align="flex-end">
              <Group justify="left">
                <Button type="submit">検索</Button>
                <Button onClick={handleReset} variant="light">
                  リセット
                </Button>
              </Group>
            </Grid.Col>
          </Grid>
        </form>
      </Card>

      {error && (
        <Alert color="red" title="エラー">
          {error.message}
        </Alert>
      )}

      <Card withBorder padding={0} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />

        <ScrollArea
          h={700}
          onScrollPositionChange={({ y }) => setScrolled(y !== 0)}
        >
          <Box w={1800}>
            <Table striped highlightOnHover verticalSpacing="sm">
              <Table.Thead
                className={`${classes.header} ${scrolled ? classes.scrolled : ""}`}
              >
                <Table.Tr>
                  <Table.Th>ID</Table.Th>
                  <Table.Th>対象日From</Table.Th>
                  <Table.Th>対象日To</Table.Th>
                  <Table.Th>銘柄コード</Table.Th>
                  <Table.Th>上場銘柄</Table.Th>
                  <Table.Th>株価四本値</Table.Th>
                  <Table.Th>バリュエーション指標</Table.Th>
                  <Table.Th>財務情報</Table.Th>
                  <Table.Th>備考</Table.Th>
                  <Table.Th>DB更新日時</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>{rows}</Table.Tbody>
            </Table>
          </Box>
        </ScrollArea>
      </Card>

      <Group justify="center">
        <Pagination
          total={totalPages}
          value={page}
          onChange={handlePageChange}
        />
      </Group>
    </Stack>
  );
};

export default CacheMgmtList;
