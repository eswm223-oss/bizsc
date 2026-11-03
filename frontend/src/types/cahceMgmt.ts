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

export type CacheMgmtRecord = {
  id: string;
  from_date: Date;
  to_date: Date;
  company_code: string | undefined;
  status_master: "Complete" | "Waiting" | "Running" | "Error" | undefined;
  status_dailyBar: "Complete" | "Waiting" | "Running" | "Error" | undefined;
  status_valuation: "Complete" | "Waiting" | "Running" | "Error" | undefined;
  status_summary: "Complete" | "Waiting" | "Running" | "Error" | undefined;
  remarks: string | undefined;
  updated_at: Date;
};

export type CacheMgmtListResponse = {
  data: CacheMgmtRecord[];
  total: number;
};

export type CacheRunRequest = {
  fromDate: Date | undefined;
  toDate: Date | undefined;
  mgmtId: string | undefined;
  code: string | undefined;
};

export type CacheRunResponse = {
  message: string | undefined;
  mgmtId: string | undefined;
};
