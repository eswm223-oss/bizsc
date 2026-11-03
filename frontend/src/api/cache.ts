import type {
  CacheRunResponse,
  CacheRunRequest,
  CacheMgmtListResponse,
  CacheMgmtRecord,
} from "../types/cacheMgmt";
import apiClient from "./client";

//***************************** */
//キャッシュ処理  開始
//***************************** */
export async function runCacheBatch(
  request: CacheRunRequest,
): Promise<CacheRunResponse> {
  const response = await apiClient.post<CacheRunResponse>(
    "/batches/jquants/cache/start",
    request,
  );
  return response.data;
}

//***************************** */
//キャッシュ処理  管理
//***************************** */
// getリスト
export async function getCacheMgmt(
  keyword?: string | null,
  date?: string | null,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<CacheMgmtListResponse> {
  const response = await apiClient.get<CacheMgmtListResponse>(
    "/cachemgmt/list",
    {
      params: {
        keyword: keyword,
        date: date,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: page,
        limit: limit,
      },
    },
  );
  return response.data;
}

// getレコード
export async function getCacheMgmtById(
  mgmtId: string | undefined,
): Promise<CacheMgmtRecord> {
  const response = await apiClient.get<CacheMgmtRecord>(`/cachemgmt/${mgmtId}`);
  return response.data;
}

// 削除
export async function deleteCacheMgmt(mgmtId: string): Promise<void> {
  await apiClient.delete(`/cachemgmt/${mgmtId}`);
}
