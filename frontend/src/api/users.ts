import apiClient from "./client";
import type {
  UserListResponse,
  User,
  UserCreate,
  UserUpdate,
} from "../types/user";

//***************************** */
//取得
//***************************** */
export async function getUsers(
  search?: string,
  isActive?: boolean,
  sortBy?: string,
  sortOrder?: string,
): Promise<UserListResponse> {
  const response = await apiClient.get<UserListResponse>("/users", {
    params: {
      search,
      is_active: isActive,
      sort_by: sortBy,
      sort_order: sortOrder,
    },
  });

  return response.data;
}

export async function getUser(id: number): Promise<User> {
  const response = await apiClient.get<User>(`/users/${id}`);

  return response.data;
}

//***************************** */
//作成
//***************************** */
export async function createUser(userCreate: UserCreate): Promise<User> {
  const response = await apiClient.post<User>("/users", userCreate);

  return response.data;
}

//***************************** */
//更新
//***************************** */
export async function updateUser(
  userId: number,
  userUpdate: UserUpdate,
): Promise<User> {
  const response = await apiClient.patch<User>(`/users/${userId}`, userUpdate);

  return response.data;
}

//***************************** */
//削除
//***************************** */
export async function deleteUser(userId: number): Promise<void> {
  await apiClient.delete(`/users/${userId}`);
}
