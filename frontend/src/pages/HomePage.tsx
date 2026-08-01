import Button from "../components/Button/Button";
import Card from "../components/Card/Card";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import Input from "../components/Input/Input";
import Loading from "../components/Loading/Loading";

function HomePage() {
  const handleClick = () => {
    alert("登録ボタンがクリックされました");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "24px",
        maxWidth: "500px",
      }}
    >
      <Card title="ユーザー登録">
        <Input
          id="email"
          label="メールアドレス"
          type="email"
          placeholder="example@example.com"
        />

        <Input
          id="password"
          label="パスワード"
          type="password"
          placeholder="8文字以上で入力してください"
        />

        <Button onClick={handleClick}>登録</Button>
      </Card>

      <Card title="読み込み表示">
        <Loading />
        <Loading message="ユーザー情報を取得しています..." />
      </Card>

      <Card title="エラー表示">
        <ErrorMessage message="ユーザー情報の取得に失敗しました。" />
      </Card>
    </div>
  );
}

export default HomePage;
