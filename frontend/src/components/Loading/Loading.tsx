type LoadingProps = {
  message?: string;
};

function Loading({ message = "読み込み中..." }: LoadingProps) {
  return (
    <div
      className="d-flex align-items-center justify-content-center gap-2 p-4 text-secondary"
      role="status"
      aria-live="polite"
    >
      <div
        className="spinner-border spinner-border-sm text-primary"
        aria-hidden="true"
      />
      <span>{message}</span>
    </div>
  );
}

export default Loading;
