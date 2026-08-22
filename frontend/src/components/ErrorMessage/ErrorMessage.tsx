type ErrorMessageProps = {
  message: string;
};

function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="alert alert-danger" role="alert">
      {message}
    </div>
  );
}

export default ErrorMessage;
