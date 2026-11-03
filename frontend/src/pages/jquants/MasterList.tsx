import React, { useState } from "react";
import { getMaster } from "../../api/jquants";
import type { Master, SearchRequest } from "../../types/jquants";
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
} from "@mantine/core";
import classes from "../TableScrollArea.module.css";
import { DatePresetsInput } from "../../components/Input/DatePresetsInput";

const MasterList = () => {
  const [searchRequest, setSearchRequest] = useState<SearchRequest>({
    keyword: undefined,
    date: null,
  });
  const [searchAppliedRequest, setSearchAppliedRequest] =
    useState<SearchRequest>({ keyword: undefined, date: null });
  const [sortBy] = useState("id");
  const [sortOrder] = useState("asc");
  const [page, setPage] = useState(1);
  const [limit] = useState(50);
  const [scrolled, setScrolled] = useState(false);

  function formatDateTime(value: string | undefined) {
    if (!value) return "";
    return new Date(value).toLocaleString("ja-JP");
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
    const result = await getMaster(
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
  const data: Master[] = response?.data ?? [];
  const total = response?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));

  // リストデータ
  const rows = data.map((row) => (
    <Table.Tr key={row.id}>
      <Table.Td>{row.date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.code}</Table.Td>
      <Table.Td>{row.company_name}</Table.Td>
      <Table.Td>{row.company_name_en}</Table.Td>
      <Table.Td>{row.sector17_code}</Table.Td>
      <Table.Td>{row.sector17_name}</Table.Td>
      <Table.Td>{row.sector33_code}</Table.Td>
      <Table.Td>{row.sector33_name}</Table.Td>
      <Table.Td>{row.scale_category}</Table.Td>
      <Table.Td>{row.market_code}</Table.Td>
      <Table.Td>{row.market_name}</Table.Td>
      <Table.Td>{row.margin_code}</Table.Td>
      <Table.Td>{row.margin_name}</Table.Td>
      <Table.Td>{row.product_category}</Table.Td>
      <Table.Td>{formatDateTime(row.created_at?.toString())}</Table.Td>
      <Table.Td>{formatDateTime(row.updated_at?.toString())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-end">
        <div>
          <Title order={2}>上場銘柄一覧</Title>
          <Text c="dimmed" size="sm" mt={4}>
            {total} 件
          </Text>
        </div>
      </Group>

      <Card withBorder padding="md" radius="md">
        <form onSubmit={handleSearch}>
          <Grid>
            <Grid.Col span={{ base: 12, md: 5, lg: 3 }} align="flex-end">
              <TextInput
                label="キーワード"
                placeholder="キーワードで検索"
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
                  <Table.Th>情報適用年月日</Table.Th>
                  <Table.Th>銘柄コード</Table.Th>
                  <Table.Th>会社名</Table.Th>
                  <Table.Th>会社名（英語）</Table.Th>
                  <Table.Th>17業種コード</Table.Th>
                  <Table.Th>17業種コード名</Table.Th>
                  <Table.Th>33業種コード</Table.Th>
                  <Table.Th>33業種コード名</Table.Th>
                  <Table.Th>規模コード</Table.Th>
                  <Table.Th>市場区分コード</Table.Th>
                  <Table.Th>市場区分名</Table.Th>
                  <Table.Th>貸借信用区分</Table.Th>
                  <Table.Th>貸借信用区分名</Table.Th>
                  <Table.Th>商品区分コード</Table.Th>
                  <Table.Th>DB登録日時</Table.Th>
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

export default MasterList;
