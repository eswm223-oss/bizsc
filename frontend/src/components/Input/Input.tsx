import type { InputHTMLAttributes } from "react";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

function Input({ label, error, id, className = "", ...props }: InputProps) {
  return (
    <div className="mb-3">
      {label && (
        <label className="form-label" htmlFor={id}>
          {label}
        </label>
      )}

      <input
        id={id}
        className={`form-control ${error ? "is-invalid" : ""} ${className}`.trim()}
        {...props}
      />

      {error && <div className="invalid-feedback">{error}</div>}
    </div>
  );
}

export default Input;
