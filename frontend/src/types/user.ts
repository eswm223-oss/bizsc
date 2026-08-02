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

//PATCH は、ユーザーのすべての項目ではなく、変更したい項目だけ送信する
export type UserUpdate = {
  email: string;
  password?: string;
  is_active?: boolean;
};
