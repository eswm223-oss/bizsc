import type { HTMLAttributes, ReactNode } from "react";
import "./Card.css";

type CardProps = HTMLAttributes<HTMLDivElement> & {
  title?: string;
  children: ReactNode;
};

function Card({ title, children, className = "", ...props }: CardProps) {
  return (
    <section className={`card ${className}`.trim()} {...props}>
      {title && <h2 className="card__title">{title}</h2>}

      <div className="card__content">{children}</div>
    </section>
  );
}

export default Card;
