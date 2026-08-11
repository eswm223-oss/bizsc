import type { ReactNode } from "react";

import "./Badge.css";

type BadgeVariant = "success" | "neutral";

type BadgeProps = {
  children: ReactNode;
  variant?: BadgeVariant;
};

function Badge({ children, variant = "neutral" }: BadgeProps) {
  return <span className={`badge badge--${variant}`}>{children}</span>;
}

export default Badge;
