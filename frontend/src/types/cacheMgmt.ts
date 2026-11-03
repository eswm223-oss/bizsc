export type CacheBatchRequest = {
  fromDate: Date;
  toDate: Date;
  mgmtId: string | undefined;
  code: string;
};

export type SearchRequest = {
  keyword: string | undefined;
  date: string | null;
};

export type CacheStatus = "Complete" | "Waiting" | "Running" | "Error";

export type CacheMgmtRecord = {
  id: string;
  from_date: string;
  to_date: string;
  company_code: string | null;
  status_master: CacheStatus | null;
  status_dailyBar: CacheStatus | null;
  status_valuation: CacheStatus | null;
  status_summary: CacheStatus | null;
  remarks: string | null;
  updated_at: string;
};

export type CacheMgmtListResponse = {
  data: CacheMgmtRecord[];
  total: number;
};

export type CacheRunRequest = {
  fromDate: string | undefined;
  toDate: string | undefined;
  mgmtId: string | undefined;
  code: string | undefined;
};

export type CacheRunResponse = {
  message: string | undefined;
  mgmtId: string | undefined;
};
