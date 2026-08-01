import "./Loading.css";

type LoadingProps = {
  message?: string;
};

function Loading({ message = "読み込み中..." }: LoadingProps) {
  return (
    <div className="loading" role="status" aria-live="polite">
      <span className="loading__spinner" aria-hidden="true" />
      <span>{message}</span>
    </div>
  );
}

export default Loading;
