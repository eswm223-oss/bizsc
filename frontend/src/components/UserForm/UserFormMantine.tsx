import type { FormEvent } from "react";
import {
  Button,
  Group,
  PasswordInput,
  Stack,
  Switch,
  TextInput,
} from "@mantine/core";

type UserFormMantineProps = {
  email: string;
  onEmailChange: (value: string) => void;
  emailError?: string;
  password?: string;
  onPasswordChange?: (value: string) => void;
  passwordError?: string;
  isActive?: boolean;
  onIsActiveChange?: (value: boolean) => void;
  isSubmitting: boolean;
  submitLabel: string;
  submittingLabel: string;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onCancel: () => void;
};

function UserFormMantine({
  email,
  onEmailChange,
  emailError,
  password,
  onPasswordChange,
  passwordError,
  isActive,
  onIsActiveChange,
  isSubmitting,
  submitLabel,
  submittingLabel,
  onSubmit,
  onCancel,
}: UserFormMantineProps) {
  return (
    <form onSubmit={onSubmit}>
      <Stack>
        <TextInput
          label="メールアドレス"
          type="email"
          value={email}
          onChange={(event) => onEmailChange(event.currentTarget.value)}
          error={emailError}
          autoComplete="email"
          disabled={isSubmitting}
          required
        />

        {password !== undefined && onPasswordChange && (
          <PasswordInput
            label="パスワード"
            value={password}
            onChange={(event) => onPasswordChange(event.currentTarget.value)}
            error={passwordError}
            autoComplete="new-password"
            disabled={isSubmitting}
            required
          />
        )}

        {isActive !== undefined && onIsActiveChange && (
          <Switch
            label="有効"
            checked={isActive}
            onChange={(event) =>
              onIsActiveChange(event.currentTarget.checked)
            }
            disabled={isSubmitting}
          />
        )}

        <Group justify="flex-end" mt="sm">
          <Button
            type="button"
            variant="default"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            キャンセル
          </Button>
          <Button type="submit" loading={isSubmitting}>
            {isSubmitting ? submittingLabel : submitLabel}
          </Button>
        </Group>
      </Stack>
    </form>
  );
}

export default UserFormMantine;
