import type { InputHTMLAttributes } from "react";
import "./Input.css";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

function Input({ label, error, id, className = "", ...props }: InputProps) {
  return (
    <div className="input-field">
      {label && (
        <label className="input-field__label" htmlFor={id}>
          {label}
        </label>
      )}

      <input
        id={id}
        className={`input-field__input ${
          error ? "input-field__input--error" : ""
        } ${className}`.trim()}
        {...props}
      />

      {error && <p className="input-field__error">{error}</p>}
    </div>
  );
}

export default Input;
