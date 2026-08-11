import type { SubmitEvent } from "react";

import Button from "../Button/Button";
import Input from "../Input/Input";
import "./UserForm.css";

type UserFormProps = {
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

  onSubmit: (event: SubmitEvent<HTMLFormElement>) => void;
};

function UserForm({
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
}: UserFormProps) {
  return (
    <form className="user-form" onSubmit={onSubmit}>
      <Input
        id="email"
        type="email"
        label="メールアドレス"
        value={email}
        onChange={(event) => onEmailChange(event.target.value)}
        error={emailError}
        autoComplete="email"
        disabled={isSubmitting}
      />

      {password !== undefined && onPasswordChange && (
        <Input
          id="password"
          type="password"
          label="パスワード"
          value={password}
          onChange={(event) => onPasswordChange(event.target.value)}
          error={passwordError}
          autoComplete="new-password"
          disabled={isSubmitting}
        />
      )}

      {isActive !== undefined && onIsActiveChange && (
        <label>
          <input
            type="checkbox"
            checked={isActive}
            onChange={(event) => onIsActiveChange(event.target.checked)}
            disabled={isSubmitting}
          />
          有効
        </label>
      )}
      <div className="user-form__actions">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? submittingLabel : submitLabel}
        </Button>
      </div>
    </form>
  );
}

export default UserForm;
