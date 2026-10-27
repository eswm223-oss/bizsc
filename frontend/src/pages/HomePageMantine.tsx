import { Link } from "react-router-dom";
import { Button, Card, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";

function HomePageMantine() {
  return (
    <Stack gap="lg">
      <div>
        <Title order={2}>ホーム</Title>
        <Text c="dimmed" mt={4}>
          ユーザー管理のサンプル画面です。
        </Text>
      </div>

      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
        <Card withBorder padding="lg" radius="md">
          <Title order={4}>ユーザー一覧</Title>
          <Text size="sm" c="dimmed" mt="xs" mb="md">
            登録済みユーザーの検索、詳細確認、削除ができます。
          </Text>
          <Group>
            <Button component={Link} to="/users">
              一覧を開く
            </Button>
          </Group>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Title order={4}>ユーザー新規登録</Title>
          <Text size="sm" c="dimmed" mt="xs" mb="md">
            メールアドレスとパスワードで新しいユーザーを登録します。
          </Text>
          <Group>
            <Button component={Link} to="/users/new" variant="light">
              新規登録
            </Button>
          </Group>
        </Card>
      </SimpleGrid>
    </Stack>
  );
}

export default HomePageMantine;
