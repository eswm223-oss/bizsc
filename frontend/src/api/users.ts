import apiClient from "./client";
import type { UserListResponse, User } from "../types/user";

export async function getUsers(): Promise<UserListResponse> {
  const response = await apiClient.get<UserListResponse>("/users");

  return response.data;
}

export async function getUser(id: number): Promise<User> {
  const response = await apiClient.get<User>(`/users/${id}`);

  return response.data;
}
