import { createTheme } from "@mantine/core";

export const theme = createTheme({
  // ボタンなどのメインカラー
  primaryColor: "blue",
  primaryShade: {
    light: 6,
    dark: 5,
  },

  // コンポーネントの角丸
  defaultRadius: "md",

  // ダークテーマのカラーを上書き
  colors: {
    dark: [
      "#f1f5f9", // 0: メイン文字色
      "#d5dfed", // 1
      "#a8b8cf", // 2: サブ文字色
      "#8195b5", // 3
      "#536989", // 4: ボーダー系
      "#344862", // 5
      "#33425a", // 6: カード背景
      "#182236", // 7: メイン背景
      "#121b2c", // 8
      "#0c1322", // 9
    ],
  },
});
