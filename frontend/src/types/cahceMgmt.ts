export type CacheBatchRequest = {
  fromDate: Date;
  toDate: Date;
  mgmtId: string | undefined;
  code: string;
};

export type CacheMgmt = {
  id: string;
  from_Date: Date;
  to_Date: Date;
  company_code: string | undefined;
  status_master: string | undefined;
  status_dailyBar: string | undefined;
  status_valuation: string | undefined;
  status_summary: string | undefined;
  remarks: string | undefined;
  upDated_at: Date;
};

export type CacheMgmtListringesponse = {
  data: CacheMgmt[];
  total: number;
};
