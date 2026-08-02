import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { isAxiosError } from "axios";

import { createUser } from "../api/users";
import Button from "../components/Button/Button";
import Card from "../components/Card/Card";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Input from "../components/Input/Input";

type ApiErrorResponse = {
  detail?: string;
};

function UserCreatePage() {
  const nabigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState<string | undefined>();
  const [passwordError, setPasswordError] = useState<string | undefined>();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    setEmailError(undefined);
    setPasswordError(undefined);
    setSubmitError(null);

    let hasError = false;

    if (!email.trim()) {
      setEmailError("メールアドレスを入力してください");
      hasError = true;
    }

    if (password.length < 8) {
      setPasswordError("パスワードは8文字以上で入力してください");
      hasError = true;
    }

    if (hasError) {
      return;
    }

    try {
      setIsSubmitting(true);

      await createUser({
        email: email.trim(),
        password: password,
      });

      nabigate("/users");
    } catch (error: unknown) {
      if (isAxiosError<ApiErrorResponse>(error)) {
        if (error.response?.status === 409) {
          setEmailError(
            error.response.data.detail ??
              "このメールアドレスはすでに登録されています",
          );
        } else if (error.response?.status === 422) {
          setSubmitError("入力内容を確認してください");
        } else {
          setSubmitError(
            error.response?.data.detail ?? "ユーザーの作成に失敗しました",
          );
        }
      } else {
        setSubmitError("予期しないエラーが発生しました");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Card title="ユーザ新規登録">
      {submitError && <ErrorMessage message={submitError} />}

      <form onSubmit={handleSubmit}>
        <Input
          id="email"
          type="email"
          label="メールアドレス"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          error={emailError}
          autoComplete="email"
          disabled={isSubmitting}
        />

        <Input
          id="password"
          type="password"
          label="パスワード"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          error={passwordError}
          autoComplete="new-password"
          disabled={isSubmitting}
        />

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "作成中..." : "作成"}
        </Button>

        <Link to="/users">キャンセル</Link>
      </form>
    </Card>
  );
}

export default UserCreatePage;
