import type { ReactNode } from "react";

type BadgeVariant = "success" | "neutral";

type BadgeProps = {
  children: ReactNode;
  variant?: BadgeVariant;
};

function Badge({ children, variant = "neutral" }: BadgeProps) {
  const bootstrapVariant = variant === "success" ? "success" : "secondary";

  return (
    <span className={`badge text-bg-${bootstrapVariant}`}>{children}</span>
  );
}

export default Badge;
