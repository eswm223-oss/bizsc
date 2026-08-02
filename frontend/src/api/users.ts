import apiClient from "./client";
import type { UserListResponse, User, UserCreate } from "../types/user";

export async function getUsers(): Promise<UserListResponse> {
  const response = await apiClient.get<UserListResponse>("/users");

  return response.data;
}

export async function getUser(id: number): Promise<User> {
  const response = await apiClient.get<User>(`/users/${id}`);

  return response.data;
}

export async function createUser(userCreate: UserCreate): Promise<User> {
  const response = await apiClient.post<User>("/users", userCreate);

  return response.data;
}
