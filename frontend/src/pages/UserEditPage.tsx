import { useEffect, useState, type SubmitEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { AxiosError } from "axios";

import { getUser, updateUser } from "../api/users";
import Card from "../components/Card/Card";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Loading from "../components/Loading/Loading";
import type { User } from "../types/user";
import UserForm from "../components/UserForm/UserForm";

function UserEditPage() {
  const { userId } = useParams();
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [email, setEmail] = useState("");
  const [isActive, setIsActive] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailError, setEmailError] = useState<string | undefined>();
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchUser() {
      if (!userId) {
        setSubmitError("ユーザーIDを取得できませんでした。");
        setIsLoading(false);
        return;
      }

      try {
        const fetchedUser = await getUser(Number(userId));

        setUser(fetchedUser);
        setEmail(fetchedUser.email);
        setIsActive(fetchedUser.is_active);
      } catch {
        setSubmitError("ユーザー情報の取得に失敗しました。");
      } finally {
        setIsLoading(false);
      }
    }

    fetchUser();
  }, [userId]);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    setEmailError(undefined);
    setSubmitError(null);

    if (!email.trim()) {
      setEmailError("メールアドレスを入力してください。");
      return;
    }

    if (!userId) {
      setSubmitError("ユーザーIDを取得できませんでした。");
      return;
    }

    try {
      setIsSubmitting(true);

      await updateUser(Number(userId), {
        email: email.trim(),
        is_active: isActive,
      });

      navigate(`/users/${userId}`);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 409) {
          setEmailError("このメールアドレスは既に登録されています。");
          return;
        }

        if (error.response?.status === 422) {
          setSubmitError("入力内容を確認してください。");
          return;
        }
      }

      setSubmitError("ユーザーの更新に失敗しました。");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return <Loading />;
  }

  if (!user) {
    return (
      <ErrorMessage message={submitError ?? "ユーザーが見つかりません。"} />
    );
  }

  return (
    <Card title="ユーザー編集">
      <UserForm
        email={email}
        onEmailChange={setEmail}
        emailError={emailError}
        isActive={isActive}
        onIsActiveChange={setIsActive}
        isSubmitting={isSubmitting}
        submitLabel="更新"
        submittingLabel="更新中..."
        onSubmit={handleSubmit}
      />
    </Card>
  );
}

export default UserEditPage;
