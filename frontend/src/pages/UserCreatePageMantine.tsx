import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, Card, Stack, Title } from "@mantine/core";
import { isAxiosError } from "axios";

import { createUser } from "../api/users";
import UserFormMantine from "../components/UserForm/UserFormMantine";

type ApiErrorResponse = {
  detail?: string;
};

function UserCreatePageMantine() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState<string | undefined>();
  const [passwordError, setPasswordError] = useState<string | undefined>();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
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
        password,
      });

      navigate("/users");
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
    <Stack gap="lg" maw={560}>
      <Title order={2}>ユーザー新規登録</Title>

      {submitError && (
        <Alert color="red" title="エラー">
          {submitError}
        </Alert>
      )}

      <Card withBorder padding="lg" radius="md">
        <UserFormMantine
          email={email}
          onEmailChange={setEmail}
          emailError={emailError}
          password={password}
          onPasswordChange={setPassword}
          passwordError={passwordError}
          isSubmitting={isSubmitting}
          submitLabel="作成"
          submittingLabel="作成中..."
          onSubmit={(event) => void handleSubmit(event)}
          onCancel={() => navigate("/users")}
        />
      </Card>
    </Stack>
  );
}

export default UserCreatePageMantine;
