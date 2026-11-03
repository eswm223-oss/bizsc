import { useState } from "react";
import {
  IconHome,
  // IconUser,
  IconUsers,
  IconBuildings,
  IconChartBar,
  IconFiles,
  IconAlignLeft2,
  IconDatabaseImport,
} from "@tabler/icons-react";
import {
  SegmentedControl,
  AppShell,
  NavLink as MantineNavLink,
  Divider,
} from "@mantine/core";
import classes from "./NavbarSegmented.module.css";
import { NavLink, useLocation } from "react-router-dom";

const tabs = {
  account: [
    { link: "/", label: "Home", icon: IconHome, end: true, top: true },
    { link: "/users", label: "User", icon: IconUsers },
  ],
  general: [
    {
      link: "/jquants/cache",
      label: "キャッシュ処理",
      icon: IconDatabaseImport,
      end: true,
      top: true,
    },
    {
      link: "/jquants/master",
      label: "上場銘柄一覧",
      icon: IconBuildings,
    },
    { link: "/jquants/dailyquote", label: "株価四本値", icon: IconChartBar },
    {
      link: "/jquants/valuation",
      label: "バリュエーション指標",
      icon: IconAlignLeft2,
    },
    { link: "/jquants/summary", label: "財務情報", icon: IconFiles },
  ],
};
interface Props {
  closeMobile: () => void;
}

export function Navbar({ closeMobile }: Props) {
  const [section, setSection] = useState<"account" | "general">("account");
  const location = useLocation();
  const links = tabs[section].map((item) => {
    const active = item.end
      ? location.pathname === item.link
      : location.pathname === item.link ||
        location.pathname.startsWith(`${item.link}/`);

    return (
      <>
        <MantineNavLink
          key={item.link}
          component={NavLink}
          to={item.link}
          leftSection={<item.icon />}
          label={item.label}
          active={active}
          onClick={closeMobile}
        />
        {item.top ? <Divider size="xs" /> : ""}
      </>
    );
  });

  return (
    <AppShell.Navbar p="md">
      <nav className={classes.navbar}>
        <div>
          <SegmentedControl
            value={section}
            onChange={(value) => setSection(value)}
            transitionTimingFunction="ease"
            fullWidth
            data={[
              { label: "Main", value: "account" },
              { label: "Data", value: "general" },
            ]}
          />
        </div>

        <div className={classes.navbarMain}>{links}</div>
      </nav>
    </AppShell.Navbar>
  );
}
