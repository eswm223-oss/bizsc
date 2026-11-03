import React, { useState } from "react";
import { getSummary } from "../../api/jquants";
import type { Summary, SearchRequest } from "../../types/jquants";
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

const SummaryList = () => {
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
    const result = await getSummary(
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
  const data: Summary[] = response?.data ?? [];
  const total = response?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));

  // リストデータ
  const rows = data.map((row) => (
    <Table.Tr key={row.id}>
      <Table.Td>{row.disclosure_date?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.disclosure_time}</Table.Td>
      <Table.Td>{row.code}</Table.Td>
      <Table.Td>{row.disclosure_number}</Table.Td>
      <Table.Td>{row.document_type}</Table.Td>
      <Table.Td>{row.current_period_type}</Table.Td>
      <Table.Td>{row.current_period_start?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>{row.current_period_end?.toLocaleString("ja-JP")}</Table.Td>
      <Table.Td>
        {row.current_fiscal_year_start?.toLocaleString("ja-JP")}
      </Table.Td>
      <Table.Td>
        {row.current_fiscal_year_end?.toLocaleString("ja-JP")}
      </Table.Td>
      <Table.Td>{row.sales?.toString()}</Table.Td>
      <Table.Td>{row.operating_profit?.toString()}</Table.Td>
      <Table.Td>{row.ordinary_profit?.toString()}</Table.Td>
      <Table.Td>{row.net_profit?.toString()}</Table.Td>
      <Table.Td>{row.eps?.toString()}</Table.Td>
      <Table.Td>{row.diluted_eps?.toString()}</Table.Td>
      <Table.Td>{row.total_assets?.toString()}</Table.Td>
      <Table.Td>{row.equity?.toString()}</Table.Td>
      <Table.Td>{row.shareholders_equity?.toString()}</Table.Td>
      <Table.Td>{row.equity_ratio?.toString()}</Table.Td>
      <Table.Td>{row.bps?.toString()}</Table.Td>
      <Table.Td>{row.roe?.toString()}</Table.Td>
      <Table.Td>{row.cash_flow_operating?.toString()}</Table.Td>
      <Table.Td>{row.cash_flow_investing?.toString()}</Table.Td>
      <Table.Td>{row.cash_flow_financing?.toString()}</Table.Td>
      <Table.Td>{row.cash_and_equivalents?.toString()}</Table.Td>
      <Table.Td>{row.dividend_annual?.toString()}</Table.Td>
      <Table.Td>{row.forecast_dividend_annual?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_dividend_annual?.toString()}</Table.Td>
      <Table.Td>{row.annual_payout_ratio?.toString()}</Table.Td>
      <Table.Td>{row.forecast_annual_payout_ratio?.toString()}</Table.Td>
      <Table.Td>{row.shares_outstanding?.toString()}</Table.Td>
      <Table.Td>{row.treasury_shares?.toString()}</Table.Td>
      <Table.Td>{row.average_shares?.toString()}</Table.Td>
      <Table.Td>{row.forecast_sales_2q?.toString()}</Table.Td>
      <Table.Td>{row.forecast_operating_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.forecast_ordinary_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.forecast_net_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.forecast_eps_2q?.toString()}</Table.Td>
      <Table.Td>{row.forecast_sales?.toString()}</Table.Td>
      <Table.Td>{row.forecast_operating_profit?.toString()}</Table.Td>
      <Table.Td>{row.forecast_ordinary_profit?.toString()}</Table.Td>
      <Table.Td>{row.forecast_net_profit?.toString()}</Table.Td>
      <Table.Td>{row.forecast_eps?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_sales_2q?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_operating_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_ordinary_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_net_profit_2q?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_eps_2q?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_sales?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_operating_profit?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_ordinary_profit?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_net_profit?.toString()}</Table.Td>
      <Table.Td>{row.next_forecast_eps?.toString()}</Table.Td>
      <Table.Td>{formatDateTime(row.created_at?.toString())}</Table.Td>
      <Table.Td>{formatDateTime(row.updated_at?.toString())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-end">
        <div>
          <Title order={2}>財務情報</Title>
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
                label={"開示日"}
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
                  <Table.Th>開示日</Table.Th>
                  <Table.Th>開示時刻</Table.Th>
                  <Table.Th>銘柄コード</Table.Th>
                  <Table.Th>開示番号</Table.Th>
                  <Table.Th>書類種別</Table.Th>
                  <Table.Th>当会計期間の種類</Table.Th>
                  <Table.Th>当会計期間の開始日</Table.Th>
                  <Table.Th>当会計期間の終了日</Table.Th>
                  <Table.Th>当事業年度の開始日</Table.Th>
                  <Table.Th>当事業年度の終了日</Table.Th>
                  <Table.Th>売上高</Table.Th>
                  <Table.Th>営業利益</Table.Th>
                  <Table.Th>経常利益</Table.Th>
                  <Table.Th>当期純利益</Table.Th>
                  <Table.Th>EPS:1株当たり当期純利益</Table.Th>
                  <Table.Th>DEPS:潜在株式調整後1株当たり当期純利益</Table.Th>
                  <Table.Th>総資産</Table.Th>
                  <Table.Th>純資産</Table.Th>
                  <Table.Th>株主資本</Table.Th>
                  <Table.Th>自己資本比率</Table.Th>
                  <Table.Th>BPS:1株当たり純資産</Table.Th>
                  <Table.Th>ROE:自己資本利益率</Table.Th>
                  <Table.Th>CFO:営業活動によるキャッシュフロー</Table.Th>
                  <Table.Th>CFI:投資活動によるキャッシュフロー</Table.Th>
                  <Table.Th>CFF:財務活動によるキャッシュフロー</Table.Th>
                  <Table.Th>現金及び現金同等物期末残高</Table.Th>
                  <Table.Th>年間配当金</Table.Th>
                  <Table.Th>予想年間配当金</Table.Th>
                  <Table.Th>翌事業年度予想年間配当金</Table.Th>
                  <Table.Th>年間配当性向</Table.Th>
                  <Table.Th>予想年間配当性向</Table.Th>
                  <Table.Th>期末発行済株式数</Table.Th>
                  <Table.Th>期末自己株式数</Table.Th>
                  <Table.Th>期中平均株式数</Table.Th>
                  <Table.Th>第2四半期累計予想売上高</Table.Th>
                  <Table.Th>第2四半期累計予想営業利益</Table.Th>
                  <Table.Th>第2四半期累計予想経常利益</Table.Th>
                  <Table.Th>第2四半期累計予想当期純利益</Table.Th>
                  <Table.Th>第2四半期累計予想EPS</Table.Th>
                  <Table.Th>通期予想売上高</Table.Th>
                  <Table.Th>通期予想営業利益</Table.Th>
                  <Table.Th>通期予想経常利益</Table.Th>
                  <Table.Th>FNP:通期予想当期純利益</Table.Th>
                  <Table.Th>FEPS:通期予想EPS</Table.Th>
                  <Table.Th>翌事業年度第2四半期累計予想売上高</Table.Th>
                  <Table.Th>翌事業年度第2四半期累計予想営業利益</Table.Th>
                  <Table.Th>翌事業年度第2四半期累計予想経常利益</Table.Th>
                  <Table.Th>翌事業年度第2四半期累計予想当期純利益</Table.Th>
                  <Table.Th>翌事業年度第2四半期累計予想EPS</Table.Th>
                  <Table.Th>翌事業年度通期予想売上高</Table.Th>
                  <Table.Th>翌事業年度通期予想営業利益</Table.Th>
                  <Table.Th>翌事業年度通期予想経常利益</Table.Th>
                  <Table.Th>翌事業年度通期予想当期純利益</Table.Th>
                  <Table.Th>翌事業年度通期予想EPS</Table.Th>
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

export default SummaryList;
