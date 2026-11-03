import React, { useState } from "react";
import { getDailyquote } from "../../api/jquants";
import type { DailyQuote, SearchRequest } from "../../types/jquants";
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

const DailyQuoteList = () => {
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

  function formatDateTime(value: string) {
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
    queryKey: [
      "dailyQuoteList",
      searchAppliedRequest,
      sortBy,
      sortOrder,
      page,
      limit,
    ],
    queryFn: () => fetchData(),
  });

  // fetch処理
  const fetchData = async () => {
    const result = await getDailyquote(
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
  const data: DailyQuote[] = response?.data ?? [];
  const total = response?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));

  // リストデータ
  const rows = data.map((row) => (
    <Table.Tr key={row.id}>
      <Table.Td>{row.date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.code}</Table.Td>
      <Table.Td>{row.open?.toString()}</Table.Td>
      <Table.Td>{row.high?.toString()}</Table.Td>
      <Table.Td>{row.low?.toString()}</Table.Td>
      <Table.Td>{row.close?.toString()}</Table.Td>
      <Table.Td>{row.upper_limit}</Table.Td>
      <Table.Td>{row.lower_limit}</Table.Td>
      <Table.Td>{row.volume?.toString()}</Table.Td>
      <Table.Td>{row.value?.toString()}</Table.Td>
      <Table.Td>{row.adjustment_factor?.toString()}</Table.Td>
      <Table.Td>{row.adjusted_open?.toString()}</Table.Td>
      <Table.Td>{row.adjusted_high?.toString()}</Table.Td>
      <Table.Td>{row.adjusted_low?.toString()}</Table.Td>
      <Table.Td>{row.adjusted_close?.toString()}</Table.Td>
      <Table.Td>{row.adjusted_volume?.toString()}</Table.Td>
      <Table.Td>{row.ex_rights_type}</Table.Td>
      <Table.Td>{formatDateTime(row.created_at?.toString())}</Table.Td>
      <Table.Td>{formatDateTime(row.updated_at?.toString())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-end">
        <div>
          <Title order={2}>株価四本値</Title>
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
                label={"日情報適用年月日"}
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
                  <Table.Th>始値</Table.Th>
                  <Table.Th>高値</Table.Th>
                  <Table.Th>安値</Table.Th>
                  <Table.Th>終値</Table.Th>
                  <Table.Th>日通ストップ高フラグ</Table.Th>
                  <Table.Th>日通ストップ安フラグ</Table.Th>
                  <Table.Th>取引高</Table.Th>
                  <Table.Th>取引代金</Table.Th>
                  <Table.Th>調整係数</Table.Th>
                  <Table.Th>調整済み始値</Table.Th>
                  <Table.Th>調整済み高値</Table.Th>
                  <Table.Th>調整済み安値</Table.Th>
                  <Table.Th>調整済み終値</Table.Th>
                  <Table.Th>調整済み取引高</Table.Th>
                  <Table.Th>権利落種類</Table.Th>
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

export default DailyQuoteList;
