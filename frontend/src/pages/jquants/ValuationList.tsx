import React, { useState } from "react";
import { getValuation } from "../../api/jquants";
import type { Valuation, SearchRequest } from "../../types/jquants";
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

const ValuationList = () => {
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
    queryKey: ["master", searchAppliedRequest, sortBy, sortBy, page],
    queryFn: () => fetchData(),
  });

  // fetch処理
  const fetchData = async () => {
    const result = await getValuation(
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
  const data: Valuation[] = response?.data ?? [];
  const total = response?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));

  // リストデータ
  const rows = data.map((row) => (
    <Table.Tr key={row.id}>
      <Table.Td>{row.date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.code}</Table.Td>
      <Table.Td>{row.eps?.toString()}</Table.Td>
      <Table.Td>{row.forward_eps?.toString()}</Table.Td>
      <Table.Td>{row.bps?.toString()}</Table.Td>
      <Table.Td>{row.roe?.toString()}</Table.Td>
      <Table.Td>{row.forward_roe?.toString()}</Table.Td>
      <Table.Td>{row.per?.toString()}</Table.Td>
      <Table.Td>{row.forward_per?.toString()}</Table.Td>
      <Table.Td>{row.pbr?.toString()}</Table.Td>
      <Table.Td>{row.market_cap?.toString()}</Table.Td>
      <Table.Td>{formatDateTime(row.created_at?.toString())}</Table.Td>
      <Table.Td>{formatDateTime(row.updated_at?.toString())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-end">
        <div>
          <Title order={2}>バリュエーション指標</Title>
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
                  <Table.Th>EPS:1株当たり利益</Table.Th>
                  <Table.Th>FwdEPS:1株当たり利益</Table.Th>
                  <Table.Th>BPS:1株当たり純資産</Table.Th>
                  <Table.Th>ROE:自己資本利益率</Table.Th>
                  <Table.Th>FwdROE:自己資本利益率</Table.Th>
                  <Table.Th>PER:株価収益率</Table.Th>
                  <Table.Th>FwdPER:株価収益率</Table.Th>
                  <Table.Th>PBR:株価純資産倍率</Table.Th>
                  <Table.Th>MktCap:時価総額</Table.Th>
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

export default ValuationList;
