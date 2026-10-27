import { useState } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
import {
  ActionIcon,
  AppShell,
  Burger,
  Anchor,
  Group,
  NavLink as MantineNavLink,
  Text,
  Title,
  Tooltip,
  useComputedColorScheme,
  useMantineColorScheme,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

const navItems = [
  { to: "/", label: "ホーム", end: true },
  { to: "/users", label: "ユーザー" },
];

function ColorSchemeToggle() {
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme("light");
  const isDark = computedColorScheme === "dark";

  return (
    <Tooltip label={isDark ? "ライトモード" : "ダークモード"}>
      <ActionIcon
        variant="default"
        size="lg"
        aria-label="カラーテーマを切り替える"
        onClick={() => setColorScheme(isDark ? "light" : "dark")}
      >
        {isDark ? "明" : "暗"}
      </ActionIcon>
    </Tooltip>
  );
}

function MainLayoutMantine() {
  const [mobileOpened, { toggle: toggleMobile, close: closeMobile }] =
    useDisclosure(false);
  const [desktopOpened, setDesktopOpened] = useState(true);
  const location = useLocation();

  return (
    <AppShell
      header={{ height: 56 }}
      navbar={{
        width: 240,
        breakpoint: "sm",
        collapsed: { mobile: !mobileOpened, desktop: !desktopOpened },
      }}
      footer={{ height: 40 }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group>
            <Burger
              opened={mobileOpened}
              onClick={toggleMobile}
              hiddenFrom="sm"
              size="sm"
            />
            <Burger
              opened={desktopOpened}
              onClick={() => setDesktopOpened((opened) => !opened)}
              visibleFrom="sm"
              size="sm"
            />
            <Anchor component={Link} to="/" underline="never" c="inherit">
              <Title order={4}>BizSC</Title>
            </Anchor>
          </Group>
          <ColorSchemeToggle />
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        {navItems.map((item) => {
          const active = item.end
            ? location.pathname === item.to
            : location.pathname === item.to ||
              location.pathname.startsWith(`${item.to}/`);

          return (
            <MantineNavLink
              key={item.to}
              component={NavLink}
              to={item.to}
              label={item.label}
              active={active}
              onClick={closeMobile}
            />
          );
        })}
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>

      <AppShell.Footer>
        <Group h="100%" px="md" justify="center">
          <Text size="xs" c="dimmed">
            BizSC
          </Text>
        </Group>
      </AppShell.Footer>
    </AppShell>
  );
}

export default MainLayoutMantine;
