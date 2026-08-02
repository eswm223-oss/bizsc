export type User = {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type UserListResponse = {
  users: User[];
};

export type UserCreate = {
  email: string;
  password: string;
};
