import { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import {
  Alert,
  Badge,
  Button,
  Card,
  Group,
  LoadingOverlay,
  Pagination,
  Select,
  Stack,
  Table,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { getUsers } from "../../api/users";
import type { User } from "../../types/user";
import { useQuery } from "@tanstack/react-query";

const SORT_OPTIONS = [
  { value: "id", label: "ID" },
  { value: "email", label: "メールアドレス" },
  { value: "created_at", label: "作成日時" },
  { value: "updated_at", label: "更新日時" },
];

const STATUS_OPTIONS = [
  { value: "all", label: "全て" },
  { value: "true", label: "有効" },
  { value: "false", label: "無効" },
];

const ORDER_OPTIONS = [
  { value: "asc", label: "昇順" },
  { value: "desc", label: "降順" },
];

function UserListPageMantine() {
  const [search, setSearch] = useState("");
  const [appliedSearch, setAppliedSearch] = useState("");
  const [activeFilter, setActiveFilter] = useState("all");
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");
  const [page, setPage] = useState(1);
  const [limit] = useState(50);

  const { data, isLoading, error } = useQuery({
    queryKey: [
      "users",
      appliedSearch,
      activeFilter,
      sortBy,
      sortOrder,
      page,
      limit,
    ],
    queryFn: () => fetchUsers(search, activeFilter, sortBy, sortOrder, page),
  });

  const fetchUsers = useCallback(
    async (
      searchValue: string,
      activeFilterValue: string,
      sortByValue: string,
      sortOrderValue: string,
      pageValue: number,
    ) => {
      const isActive =
        activeFilterValue === "all" ? undefined : activeFilterValue === "true";

      const response = await getUsers(
        searchValue || undefined,
        isActive,
        sortByValue,
        sortOrderValue,
        pageValue,
        limit,
      );
      return response;
    },
    [limit],
  );
  const users: User[] = data?.users ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / limit));

  function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPage(1);
    setAppliedSearch(search);
  }

  function handlePageChange(nextPage: number) {
    setPage(nextPage);
  }

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-end">
        <div>
          <Title order={2}>ユーザー一覧</Title>
          <Text c="dimmed" size="sm" mt={4}>
            {total} 件
          </Text>
        </div>
        <Button component={Link} to="/users/new">
          新規登録
        </Button>
      </Group>

      <Card withBorder padding="md" radius="md">
        <form onSubmit={handleSearch}>
          <Group align="flex-end" wrap="wrap">
            <TextInput
              label="メールアドレス"
              placeholder="メールアドレスで検索"
              value={search}
              onChange={(event) => setSearch(event.currentTarget.value)}
              style={{ flex: "1 1 220px" }}
            />
            <Select
              label="ステータス"
              data={STATUS_OPTIONS}
              value={activeFilter}
              onChange={(value) => setActiveFilter(value ?? "all")}
              allowDeselect={false}
              w={140}
            />
            <Select
              label="並び替え"
              data={SORT_OPTIONS}
              value={sortBy}
              onChange={(value) => setSortBy(value ?? "id")}
              allowDeselect={false}
              w={180}
            />
            <Select
              label="順序"
              data={ORDER_OPTIONS}
              value={sortOrder}
              onChange={(value) => setSortOrder(value ?? "asc")}
              allowDeselect={false}
              w={120}
            />
            <Button type="submit">検索</Button>
          </Group>
        </form>
      </Card>

      {error && (
        <Alert color="red" title="エラー">
          {error.message}
        </Alert>
      )}

      <Card withBorder padding={0} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />
        {users.length === 0 && !isLoading ? (
          <Text ta="center" c="dimmed" py="xl">
            ユーザーが登録されていません
          </Text>
        ) : (
          <Table.ScrollContainer minWidth={640}>
            <Table striped highlightOnHover verticalSpacing="sm">
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>ID</Table.Th>
                  <Table.Th>メールアドレス</Table.Th>
                  <Table.Th>ステータス</Table.Th>
                  <Table.Th>作成日時</Table.Th>
                  <Table.Th>操作</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {users.map((user) => (
                  <Table.Tr key={user.id}>
                    <Table.Td>{user.id}</Table.Td>
                    <Table.Td>{user.email}</Table.Td>
                    <Table.Td>
                      <Badge color={user.is_active ? "green" : "gray"}>
                        {user.is_active ? "有効" : "無効"}
                      </Badge>
                    </Table.Td>
                    <Table.Td>
                      {new Date(user.created_at).toLocaleString("ja-JP")}
                    </Table.Td>
                    <Table.Td>
                      <Button
                        component={Link}
                        to={`/users/${user.id}`}
                        variant="light"
                        size="xs"
                      >
                        詳細
                      </Button>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>
        )}
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
}

export default UserListPageMantine;
