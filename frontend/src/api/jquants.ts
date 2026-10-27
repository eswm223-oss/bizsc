import apiClient from "./client";
import type { MasterListRsponse } from "../types/jquants";

//***************************** */
//取得
//***************************** */
export async function getMaster(
  search?: string,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<MasterListRsponse> {
  debugger;
  const response = await apiClient.get<MasterListRsponse>("/jquants/master", {
    params: {
      search: search,
      sort_by: sortBy,
      sort_order: sortOrder,
      page: page,
      limit: limit,
    },
  });
  return response.data;
}
