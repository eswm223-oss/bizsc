import "./ErrorMessage.css";

type ErrorMessageProps = {
  message: string;
};

function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="error-message" role="alert">
      {message}
    </div>
  );
}

export default ErrorMessage;
