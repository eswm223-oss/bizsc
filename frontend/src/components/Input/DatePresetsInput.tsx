import dayjs from "dayjs";
import { DatePickerInput } from "@mantine/dates";

type Props = {
  value: string | null;
  onChange: (value: string | null) => void;
  label?: string;
  required?: boolean;
};

export function DatePresetsInput({
  value,
  onChange,
  label = "日付",
  required = false,
}: Props) {
  const presets = [
    {
      label: "昨日",
      value: dayjs().subtract(1, "day").format("YYYY-MM-DD"),
    },
    {
      label: "今日",
      value: dayjs().format("YYYY-MM-DD"),
    },
    {
      label: "明日",
      value: dayjs().add(1, "day").format("YYYY-MM-DD"),
    },
    {
      label: "1週間前",
      value: dayjs().subtract(7, "day").format("YYYY-MM-DD"),
    },
    {
      label: "1か月前",
      value: dayjs().subtract(1, "month").format("YYYY-MM-DD"),
    },
    {
      label: "1年前",
      value: dayjs().subtract(1, "year").format("YYYY-MM-DD"),
    },
  ];

  return (
    <DatePickerInput
      label={label}
      placeholder="日付を選択"
      value={value ? dayjs(value).format("YYYY-MM-DD") : null}
      onChange={onChange}
      presets={presets}
      valueFormat="YYYY/MM/DD"
      clearable
      required={required}
    />
  );
}
