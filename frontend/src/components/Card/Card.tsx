import type { HTMLAttributes, ReactNode } from "react";

type CardProps = HTMLAttributes<HTMLDivElement> & {
  title?: string;
  children: ReactNode;
};

function Card({ title, children, className = "", ...props }: CardProps) {
  return (
    <section className={`card shadow-sm ${className}`.trim()} {...props}>
      {title && (
        <div className="card-header">
          <h2 className="h5 mb-0">{title}</h2>
        </div>
      )}

      <div className="card-body">{children}</div>
    </section>
  );
}

export default Card;
