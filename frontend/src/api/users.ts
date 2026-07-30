import apiClient from "./client";
import type { UserListResponse } from "../types/user";

export async function getUsers(): Promise<UserListResponse> {
  const response = await apiClient.get<UserListResponse>("/users");

  return response.data;
}
