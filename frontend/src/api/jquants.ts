import apiClient from "./client";
import type {
  MasterListRsponse,
  ValuationListRsponse,
  DailyQuoteListRsponse,
  SummaryListRsponse,
} from "../types/jquants";

//***************************** */
// /jquants
//***************************** */

// master
export async function getMaster(
  keyword?: string | null,
  date?: string | null,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<MasterListRsponse> {
  const response = await apiClient.get<MasterListRsponse>("/jquants/master", {
    params: {
      keyword: keyword,
      date: date,
      sort_by: sortBy,
      sort_order: sortOrder,
      page: page,
      limit: limit,
    },
  });
  return response.data;
}

// valuation
export async function getValuation(
  keyword?: string | null,
  date?: string | null,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<ValuationListRsponse> {
  const response = await apiClient.get<ValuationListRsponse>(
    "/jquants/valuation",
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

// summary
export async function getSummary(
  keyword?: string | null,
  date?: string | null,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<SummaryListRsponse> {
  const response = await apiClient.get<SummaryListRsponse>("/jquants/summary", {
    params: {
      keyword: keyword,
      date: date,
      sort_by: sortBy,
      sort_order: sortOrder,
      page: page,
      limit: limit,
    },
  });
  return response.data;
}

// dailyquote
export async function getDailyquote(
  keyword?: string | null,
  date?: string | null,
  sortBy?: string,
  sortOrder?: string,
  page?: number,
  limit?: number,
): Promise<DailyQuoteListRsponse> {
  const response = await apiClient.get<DailyQuoteListRsponse>(
    "/jquants/dailyquote",
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
