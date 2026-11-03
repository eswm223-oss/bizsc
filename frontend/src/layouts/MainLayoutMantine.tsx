import { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import {
  ActionIcon,
  AppShell,
  Burger,
  Anchor,
  Group,
  Title,
  Tooltip,
  useComputedColorScheme,
  useMantineColorScheme,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Navbar } from "../components/Navbar";
import { IconSun, IconMoon } from "@tabler/icons-react";
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
        {isDark ? <IconSun /> : <IconMoon />}
      </ActionIcon>
    </Tooltip>
  );
}

function MainLayoutMantine() {
  const [mobileOpened, { toggle: toggleMobile, close: closeMobile }] =
    useDisclosure(false);
  const [desktopOpened, setDesktopOpened] = useState(true);

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

      <Navbar closeMobile={closeMobile} />

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}

export default MainLayoutMantine;
