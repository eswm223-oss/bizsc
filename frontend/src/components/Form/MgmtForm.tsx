import type { SubmitEvent } from "react";
import { Button, Group, Stack, TextInput } from "@mantine/core";
import { DatePresetsInput } from "../Input/DatePresetsInput";

type Props = {
  fromDate: string;
  onFromDateChange: (value: string) => void;
  toDate: string;
  onToDateChange: (value: string) => void;
  companyCode: string;
  onCompnayChange: (value: string) => void;
  isSubmitting: boolean;
  onSubmit: (event: SubmitEvent<HTMLFormElement>) => void;
  submitLabel: string;
  submittingLabel: string;
  onCancel: () => void;
};

function MgmtForm({
  fromDate,
  onFromDateChange,
  toDate,
  onToDateChange,
  companyCode,
  onCompnayChange,
  isSubmitting,
  onSubmit,
  submitLabel,
  submittingLabel,
  onCancel,
}: Props) {
  return (
    <form onSubmit={onSubmit}>
      <Stack>
        <DatePresetsInput
          label="対象日From"
          value={fromDate}
          onChange={(date) => {
            onFromDateChange(date || "");
          }}
          required={true}
        />

        <DatePresetsInput
          label="対象日To"
          value={toDate}
          onChange={(date) => onToDateChange(date || "")}
          required={true}
        />

        <TextInput
          label="企業コード"
          type="text"
          value={companyCode}
          onChange={(event) => onCompnayChange(event.currentTarget.value)}
        />

        <Group justify="flex-end" mt="sm">
          <Button
            type="button"
            variant="default"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            キャンセル
          </Button>
          <Button
            type="submit"
            loading={isSubmitting}
            disabled={!fromDate || !toDate || fromDate > toDate}
          >
            {isSubmitting ? submittingLabel : submitLabel}
          </Button>
        </Group>
      </Stack>
    </form>
  );
}

export default MgmtForm;
